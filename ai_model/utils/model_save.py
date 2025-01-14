import os
import subprocess
import re
import json
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
from backend.config.logger import logger
from backend.config.config import MODEL_NAME, BASE_DIR

class GitLFSError(Exception):
    """Custom exception for Git LFS related errors"""
    def __init__(self, message: str = None, error_code: int = None, command: str = None):
        self.message = message or "Git LFS operation failed"
        self.error_code = error_code
        self.command = command
        
        detailed_msg = self.message
        if self.command:
            detailed_msg += f"\nFailed command: {self.command}"
        if self.error_code:
            detailed_msg += f"\nError code: {self.error_code}"
            
        super().__init__(detailed_msg)

class VersionLockError(Exception):
    """Custom exception for version locking related errors"""
    def __init__(self, version: str = None, reason: str = None):
        self.version = version
        self.reason = reason or "Version lock operation failed"
        
        detailed_msg = f"Version lock error for {version if version else 'unknown version'}"
        detailed_msg += f"\nReason: {self.reason}"
        
        super().__init__(detailed_msg)

class ModelSaveError(Exception):
    """Custom exception for model saving related errors"""
    def __init__(self, model_path: str = None, missing_files: list = None, error_msg: str = None):
        self.model_path = model_path
        self.missing_files = missing_files
        self.error_msg = error_msg or "Model save operation failed"
        
        detailed_msg = self.error_msg
        if self.model_path:
            detailed_msg += f"\nModel path: {self.model_path}"
        if self.missing_files:
            detailed_msg += f"\nMissing files: {', '.join(self.missing_files)}"
            
        super().__init__(detailed_msg)

class GitOperationError(Exception):
    """Custom exception for general Git operations"""
    def __init__(self, operation: str = None, stderr: str = None, repo_path: str = None):
        self.operation = operation
        self.stderr = stderr
        self.repo_path = repo_path
        
        detailed_msg = f"Git operation failed: {operation or 'unknown operation'}"
        if self.repo_path:
            detailed_msg += f"\nRepository path: {self.repo_path}"
        if self.stderr:
            detailed_msg += f"\nError details: {self.stderr}"
            
        super().__init__(detailed_msg)

def verify_lfs_tracking(local_path: str) -> bool:
    """Verify Git LFS is properly tracking files."""
    try:
        result = subprocess.run(
            ["git", "lfs", "ls-files"],
            cwd=local_path,
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.returncode != 0:
            raise GitLFSError(
                message="Git LFS command failed",
                command="git lfs ls-files",
                error_code=result.returncode
            )
        
        required_patterns = ["*.safetensors", "*.bin", "*.pt", "*.pth"]
        tracked_patterns = [line.split()[-1] for line in result.stdout.splitlines()]
        
        missing_patterns = [pat for pat in required_patterns if pat not in tracked_patterns]
        if missing_patterns:
            raise GitLFSError(
                message=f"Missing LFS patterns: {', '.join(missing_patterns)}",
                command="git lfs track verification"
            )
            
        return True
    except subprocess.CalledProcessError as e:
        raise GitLFSError(
            message="Failed to check LFS tracking",
            error_code=e.returncode,
            command=str(e.cmd)
        )

def safe_git_operation(command: list, cwd: str, operation_name: str) -> bool:
    """Safely execute a git command with proper error handling."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.returncode != 0:
            raise GitOperationError(
                operation=operation_name,
                stderr=result.stderr,
                repo_path=cwd
            )
        return True
        
    except subprocess.CalledProcessError as e:
        raise GitOperationError(
            operation=operation_name,
            stderr=e.stderr,
            repo_path=cwd
        )

def safe_pull_before_push(local_path: str) -> bool:
    """Safely pull latest changes before pushing."""
    try:
        # Stash any local changes
        stash_result = subprocess.run(
            ["git", "stash"],
            cwd=local_path,
            capture_output=True,
            text=True
        )
        
        # Pull with rebase
        pull_result = subprocess.run(
            ["git", "pull", "--rebase", "origin", "main"],
            cwd=local_path,
            capture_output=True,
            text=True
        )
        
        if pull_result.returncode != 0:
            raise GitOperationError(
                operation="pull",
                stderr=pull_result.stderr,
                repo_path=local_path
            )
        
        # Pop stash if we stashed changes
        if "No local changes to save" not in stash_result.stderr:
            subprocess.run(
                ["git", "stash", "pop"],
                cwd=local_path,
                check=True
            )
            
        return True
        
    except subprocess.CalledProcessError as e:
        raise GitOperationError(
            operation="safe_pull",
            stderr=str(e),
            repo_path=local_path
        )

def setup_git_config(local_path: str) -> bool:
    """Set up Git configuration."""
    configs = [
        ["user.email", "ai-training@example.com"],
        ["user.name", "AI Training Bot"],
        ["lfs.contenttype", "false"],
        ["core.autocrlf", "false"]
    ]
    
    for config_name, config_value in configs:
        try:
            safe_git_operation(
                ["git", "config", config_name, config_value],
                local_path,
                f"git_config_{config_name}"
            )
        except GitOperationError as e:
            logger.error(f"Failed to set git config {config_name}: {e}")
            return False
    
    return True

def lock_version(version: str, local_path: str) -> None:
    """Create a lock file for the version being created."""
    lock_file = os.path.join(local_path, f"{version}.lock")
    if os.path.exists(lock_file):
        raise VersionLockError(
            version=version,
            reason="Version is already locked"
        )
        
    lock_data = {
        "version": version,
        "timestamp": datetime.now().isoformat(),
        "locked_by": "AI Training Bot",
        "hostname": os.uname().nodename if hasattr(os, 'uname') else None,
        "pid": os.getpid()
    }
    
    try:
        with open(lock_file, 'w') as f:
            json.dump(lock_data, f, indent=2)
    except IOError as e:
        raise VersionLockError(
            version=version,
            reason=f"Failed to create lock file: {str(e)}"
        )

def setup_git_repo(repo_url: str, local_path: str) -> bool:
    try:
        subprocess.run(["git", "lfs", "install"], cwd=local_path, check=True)
        # Remove the commit attempt since attributes already exist
        return True
    except Exception as e:
        logger.error(f"Git setup failed: {e}")
        return False
   
def pull_repo(local_path: str, repo_url: str) -> bool:
    try:
        git_dir = os.path.join(local_path, '.git')
        
        if not os.path.exists(git_dir):
            logger.info(f"Cloning repo to {local_path}")
            subprocess.run(["git", "clone", repo_url, local_path], check=True)
            setup_git_config(local_path)
            return True

        logger.info("Updating existing repo")
        subprocess.run(["git", "fetch", "origin"], cwd=local_path, check=True)
        subprocess.run(["git", "reset", "--hard", "origin/main"], cwd=local_path, check=True)
        subprocess.run(["git", "clean", "-fd"], cwd=local_path, check=True)
        subprocess.run(["git", "pull"], cwd=local_path, check=True)
        
        return True
    except Exception as e:
        logger.error(f"Pull failed: {e}")
        return False

def get_next_version(models_dir: str) -> str:
    """Get the next version number with improved pattern matching."""
    try:
        if not os.path.exists(models_dir):
            return "v1.0.0"
            
        version_pattern = re.compile(r"trained_model_v(\d+)\.0\.0")
        existing_versions = []
        
        for item in os.listdir(models_dir):
            match = version_pattern.match(item)
            if match:
                version_num = int(match.group(1))
                lock_file = os.path.join(models_dir, f"v{version_num}.0.0.lock")
                if not os.path.exists(lock_file):
                    existing_versions.append(version_num)
        
        next_version = max(existing_versions, default=0) + 1
        return f"v{next_version}.0.0"
        
    except Exception as e:
        logger.error(f"Error determining next version: {e}")
        raise

def save_model(model: Any, tokenizer: Any, output_dir: str) -> None:
    """Save model and tokenizer with proper directory handling."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)
        
        # Verify files were saved
        required_files = ['config.json', 'model.safetensors', 'vocab.txt']
        missing_files = [f for f in required_files if not os.path.exists(os.path.join(output_dir, f))]
        
        if missing_files:
            raise ModelSaveError(
                model_path=output_dir,
                missing_files=missing_files,
                error_msg="Missing required files after save"
            )
            
        logger.info(f"Model and tokenizer successfully saved to {output_dir}")
        
    except Exception as e:
        raise ModelSaveError(
            model_path=output_dir,
            error_msg=str(e)
        )

def save_metrics(metrics: Dict, version: str, metrics_dir: str) -> Optional[str]:
    """Save metrics with additional metadata."""
    try:
        os.makedirs(metrics_dir, exist_ok=True)
        
        metrics_data = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "model_name": MODEL_NAME,
            "metrics": metrics,
            "environment": {
                "platform": os.uname().sysname if hasattr(os, 'uname') else os.name,
                "python_version": os.sys.version,
                "hostname": os.uname().nodename if hasattr(os, 'uname') else None
            }
        }
        
        metrics_file = os.path.join(metrics_dir, f"metrics_{version}.json")
        with open(metrics_file, 'w') as f:
            json.dump(metrics_data, f, indent=4)
            
        logger.info(f"Metrics saved to {metrics_file}")
        return metrics_file
        
    except Exception as e:
        logger.error(f"Error saving metrics: {e}")
        raise

def push_model_and_metrics(repo_path: str, version: str, model_dir: str, metrics_file: Optional[str]) -> bool:
    try:
        # Add the newly trained model files
        subprocess.run(["git", "add", f"trained_model_{version}/*"], cwd=repo_path, check=True)
        subprocess.run(["git", "add", f"metrics/metrics_{version}.json"], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", f"Add model version {version}"], cwd=repo_path, check=True)
        subprocess.run(["git", "push"], cwd=repo_path, check=True)
        return True
    except Exception as e:
        logger.error(f"Push failed: {e}")
        return False
def save_and_version_model(
   model: Any,
   tokenizer: Any, 
   models_dir: str,
   metrics: Optional[Dict] = None,
   repo_url: Optional[str] = None
) -> Tuple[str, Optional[str]]:
   lock_file = None
   try:
       os.makedirs(models_dir, exist_ok=True)

       if repo_url:
           pull_success = pull_repo(models_dir, repo_url)
           if not pull_success:
               logger.warning("Failed to pull latest changes")
           git_setup_success = setup_git_repo(repo_url, models_dir)
           if not git_setup_success:
               logger.warning("Git setup failed, continuing without versioning")

       version = get_next_version(models_dir)
       lock_version(version, models_dir)
       lock_file = os.path.join(models_dir, f"{version}.lock")
       
       model_dir = f"trained_model_{version}"
       output_dir = os.path.join(models_dir, model_dir)
       save_model(model, tokenizer, output_dir)

       metrics_file = None
       if metrics is not None:
           metrics_dir = os.path.join(models_dir, "metrics")
           metrics_file = save_metrics(metrics, version, metrics_dir)

       if repo_url and git_setup_success:
           push_success = push_model_and_metrics(models_dir, version, model_dir, metrics_file)
           if not push_success:
               logger.warning("Failed to push to remote, but model saved locally")

       return output_dir, metrics_file

   except Exception as e:
       if lock_file and os.path.exists(lock_file):
           try:
               os.remove(lock_file)
           except Exception as cleanup_error:
               logger.error(f"Failed to cleanup lock file: {cleanup_error}")
       raise

   finally:
       if lock_file and os.path.exists(lock_file):
           try:
               os.remove(lock_file)
           except Exception as cleanup_error:
               logger.error(f"Failed to cleanup lock file in finally: {cleanup_error}")