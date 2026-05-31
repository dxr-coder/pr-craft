from app.core.logger import logger
from app.github.client import repo


def create_branch(branch_name: str, base_branch: str = "main"):
    try:
        base_ref = repo.get_git_ref(f"heads/{base_branch}")
        repo.create_git_ref(f"refs/heads/{branch_name}", base_ref.object.sha)
        logger.info(f"分支{branch_name}创建成功")
    except Exception as e:
        logger.error(f"创建分支失败: {e}")
        raise


def create_file(branch_name: str, file_path: str, content: str, message: str):
    try:
        repo.create_file(
            path=file_path,
            message=message,
            content=content,
            branch=branch_name,
        )
        logger.info(f"文件 {file_path} 提交成功")
    except Exception as e:
        logger.error(f"提交文件失败: {e}")
        raise


def create_pr(title: str, body: str, branch_name: str, base_branch: str = "main"):
    try:
        pr = repo.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base=base_branch,
        )
        logger.info(f"PR 创建成功: {pr.html_url}")
        return pr.html_url
    except Exception as e:
        logger.error(f"创建 PR 失败: {e}")
        raise
