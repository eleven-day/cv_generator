import os
import sys
import subprocess
import shutil
import argparse
import logging
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("builder")

class BuildError(Exception):
    """自定义构建错误异常"""
    pass

def run_command(cmd, check=True, cwd=None, env=None, shell=False):
    """
    执行命令并处理错误
    
    Args:
        cmd: 要执行的命令（列表或字符串）
        check: 是否在命令失败时抛出异常
        cwd: 执行命令的工作目录
        env: 环境变量
        shell: 是否使用shell执行命令
        
    Returns:
        subprocess.CompletedProcess: 命令执行结果
    """
    try:
        logger.debug(f"执行命令: {cmd}")
        result = subprocess.run(
            cmd, 
            check=check, 
            cwd=cwd, 
            env=env, 
            shell=shell,
            text=True,
            capture_output=True
        )
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"命令执行失败: {e}")
        logger.error(f"错误输出: {e.stderr}")
        if check:
            raise BuildError(f"命令执行失败: {e}")
        return e

def check_dependencies():
    """检查并安装必要的依赖"""
    logger.info("检查系统依赖...")
    
    # 检查Node.js和npm
    try:
        node_version = run_command(["node", "--version"])
        npm_version = run_command(["npm", "--version"])
        logger.info(f"Node.js版本: {node_version.stdout.strip()}")
        logger.info(f"npm版本: {npm_version.stdout.strip()}")
    except (BuildError, FileNotFoundError):
        logger.error("Node.js或npm未安装，请先安装Node.js: https://nodejs.org/")
        raise BuildError("缺少Node.js依赖")
    
    # 安装Python依赖
    logger.info("安装Python依赖...")
    requirements_path = Path("backend/requirements.txt")
    if not requirements_path.exists():
        logger.error(f"找不到requirements.txt: {requirements_path}")
        raise BuildError("找不到requirements.txt文件")
    
    run_command([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])
    
    # 安装PyInstaller
    try:
        import pyinstaller
        logger.info(f"PyInstaller版本: {pyinstaller.__version__}")
    except ImportError:
        logger.info("安装PyInstaller...")
        run_command([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0"])

def build_frontend(frontend_dir="frontend", production=True):
    """
    构建React前端
    
    Args:
        frontend_dir: 前端代码目录
        production: 是否为生产环境构建
    
    Returns:
        Path: 构建输出目录路径
    """
    frontend_path = Path(frontend_dir)
    if not frontend_path.exists():
        raise BuildError(f"前端目录不存在: {frontend_path}")
    
    logger.info("构建前端应用...")
    
    # 检查package.json
    package_json = frontend_path / "package.json"
    if not package_json.exists():
        raise BuildError(f"找不到package.json: {package_json}")
    
    # 安装依赖
    node_modules = frontend_path / "node_modules"
    if not node_modules.exists():
        logger.info("安装前端依赖...")
        run_command(["npm", "install"], cwd=frontend_path)
    
    # 运行构建命令
    build_cmd = "build" if production else "build:dev"
    logger.info(f"执行npm {build_cmd}...")
    run_command(["npm", "run", build_cmd], cwd=frontend_path)
    
    build_output = frontend_path / "build"
    if not build_output.exists():
        raise BuildError(f"前端构建失败，输出目录不存在: {build_output}")
    
    return build_output

def prepare_backend(backend_dir="backend", frontend_build_dir=None):
    """
    准备后端应用
    
    Args:
        backend_dir: 后端代码目录
        frontend_build_dir: 前端构建输出目录
    """
    backend_path = Path(backend_dir)
    if not backend_path.exists():
        raise BuildError(f"后端目录不存在: {backend_path}")
    
    logger.info("准备后端应用...")
    
    # 复制前端构建到后端静态目录
    if frontend_build_dir:
        static_dir = backend_path / "app" / "static"
        if static_dir.exists():
            logger.info(f"清理现有静态资源目录: {static_dir}")
            shutil.rmtree(static_dir)
        
        logger.info(f"复制前端构建到后端静态目录: {static_dir}")
        static_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(frontend_build_dir, static_dir, dirs_exist_ok=True)

def create_entry_script(build_dir, custom_port=8000):
    """
    创建应用入口脚本
    
    Args:
        build_dir: 构建目录
        custom_port: 应用使用的端口
    
    Returns:
        Path: 入口脚本路径
    """
    build_path = Path(build_dir)
    build_path.mkdir(exist_ok=True, parents=True)
    
    entry_script = build_path / "resume_generator.py"
    logger.info(f"创建应用入口脚本: {entry_script}")
    
    entry_script_content = f"""
    import os
    import sys
    import uvicorn
    import webbrowser
    import logging
    from threading import Timer
    from pathlib import Path

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("resume-generator")

    def open_browser():
        \"\"\"打开浏览器访问应用\"\"\"
        url = f"http://localhost:{custom_port}"
        logger.info(f"正在浏览器中打开应用: {{url}}")
        webbrowser.open(url)

    # 应用配置
    PORT = {custom_port}
    HOST = "127.0.0.1"  # 只允许本地访问更安全

    if __name__ == "__main__":
        logger.info("正在启动简历生成器应用...")
        
        # 获取应用路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            application_path = Path(sys.executable).parent
        else:
            # 如果是开发环境
            application_path = Path(__file__).parent
        
        # 设置工作目录
        os.chdir(application_path)
        
        # 添加后端模块到Python路径
        backend_path = application_path
        if not getattr(sys, 'frozen', False):
            backend_path = Path(__file__).parent.parent
        sys.path.insert(0, str(backend_path))
        
        # 在短暂延迟后打开浏览器
        Timer(2, open_browser).start()
        
        try:
            # 导入并运行FastAPI应用
            logger.info(f"启动API服务于: {{HOST}}:{{PORT}}")
            from backend.app.main import app
            uvicorn.run(app, host=HOST, port=PORT)
        except Exception as e:
            logger.error(f"应用启动失败: {{e}}")
            input("按回车键退出...")
    """

    with open(entry_script, "w") as f:
        f.write(entry_script_content)
    
    return entry_script

def build_executable(entry_script, output_dir, app_name, icon_path=None, clean_build=True):
    """
    使用PyInstaller构建可执行文件
    
    Args:
        entry_script: 入口脚本路径
        output_dir: 输出目录
        app_name: 应用名称
        icon_path: 图标路径
        clean_build: 是否清理构建文件
    
    Returns:
        Path: 可执行文件路径
    """
    logger.info("使用PyInstaller构建可执行文件...")
    
    # 确定构建目录
    build_dir = Path("build")
    dist_dir = Path(output_dir) / "dist"
    
    # 准备PyInstaller命令
    pyinstaller_cmd = [
        "pyinstaller",
        "--name", app_name,
        "--onefile",
        "--windowed" if sys.platform in ["win32", "darwin"] else "--console",
        "--add-data", f"../backend/app/static{os.pathsep}app/static",
        "--clean" if clean_build else "",
        "--noconfirm",
        "--distpath", str(dist_dir),
    ]
    
    # 添加图标
    if icon_path and Path(icon_path).exists():
        logger.info(f"使用图标: {icon_path}")
        pyinstaller_cmd.extend(["--icon", icon_path])
    else:
        logger.warning(f"图标不存在或未指定: {icon_path}")
    
    # 移除空字符串
    pyinstaller_cmd = [cmd for cmd in pyinstaller_cmd if cmd]
    
    # 添加入口脚本
    pyinstaller_cmd.append(str(entry_script.name))
    
    # 确保输出目录存在
    dist_dir.parent.mkdir(exist_ok=True, parents=True)
    
    # 运行PyInstaller
    run_command(pyinstaller_cmd, cwd=build_dir)
    
    # 确定可执行文件名称和路径
    if sys.platform == "win32":
        exe_name = f"{app_name}.exe"
    elif sys.platform == "darwin":
        exe_name = app_name + ".app"
    else:  # Linux
        exe_name = app_name
    
    executable_path = dist_dir / exe_name
    
    if not executable_path.exists():
        raise BuildError(f"构建失败，可执行文件不存在: {executable_path}")
    
    return executable_path

def copy_to_output(executable_path, output_dir):
    """
    复制可执行文件到输出目录
    
    Args:
        executable_path: 可执行文件路径
        output_dir: 输出目录
    
    Returns:
        Path: 最终可执行文件路径
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    dest_path = output_path / executable_path.name
    
    logger.info(f"复制可执行文件到输出目录: {dest_path}")
    if dest_path.exists():
        dest_path.unlink()
    
    shutil.copy2(executable_path, dest_path)
    
    return dest_path

def clean_temp_files(build_dir="build", keep_dist=False):
    """
    清理临时构建文件
    
    Args:
        build_dir: 构建目录
        keep_dist: 是否保留dist目录
    """
    build_path = Path(build_dir)
    
    if not build_path.exists():
        return
    
    logger.info("清理临时构建文件...")
    
    # 清理临时构建文件和目录
    for item in build_path.iterdir():
        if item.name == "dist" and keep_dist:
            continue
        
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

def create_config_file(app_name, version="1.0.0"):
    """
    创建应用配置文件
    
    Args:
        app_name: 应用名称
        version: 应用版本
    """
    config = {
        "name": app_name,
        "version": version,
        "buildTime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "platform": sys.platform
    }
    
    config_dir = Path("build")
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "app_config.json"
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    
    return config_file

def build_app(output_dir, app_name="Resume Generator", clean=True, port=8000):
    """
    构建应用主函数
    
    Args:
        output_dir: 输出目录
        app_name: 应用名称
        clean: 是否清理临时文件
        port: 应用端口
    """
    start_time = time.time()
    logger.info(f"开始构建 {app_name}...")
    
    try:
        # 创建构建目录
        build_dir = Path("build")
        build_dir.mkdir(exist_ok=True)
        
        # 初始化构建环境
        check_dependencies()
        
        # 创建配置文件
        create_config_file(app_name)
        
        # 并行构建前端和准备后端环境
        with ThreadPoolExecutor() as executor:
            # 构建前端
            frontend_future = executor.submit(build_frontend)
            
            # 等待前端构建完成
            frontend_build_dir = frontend_future.result()
        
        # 使用构建好的前端准备后端
        prepare_backend(frontend_build_dir=frontend_build_dir)
        
        # 创建应用入口脚本
        entry_script = create_entry_script(build_dir, custom_port=port)
        
        # 找到图标
        icon_path = None
        favicon_path = Path("frontend/public/favicon.ico")
        if favicon_path.exists():
            icon_path = str(favicon_path)
        
        # 构建可执行文件
        executable_path = build_executable(
            entry_script=entry_script,
            output_dir=output_dir,
            app_name=app_name,
            icon_path=icon_path,
            clean_build=clean
        )
        
        # 复制到输出目录
        final_path = copy_to_output(executable_path, output_dir)
        
        # 清理临时文件
        if clean:
            clean_temp_files(keep_dist=False)
        
        elapsed_time = time.time() - start_time
        logger.info(f"构建完成! 用时: {elapsed_time:.2f}秒")
        logger.info(f"可执行文件位置: {final_path}")
        
        return final_path
    
    except BuildError as e:
        logger.error(f"构建失败: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"构建过程中出现未预期的错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="构建简历生成器应用")
    parser.add_argument("--output", default="dist", help="可执行文件输出目录")
    parser.add_argument("--name", default="Resume Generator", help="应用名称")
    parser.add_argument("--no-clean", action="store_true", help="保留临时构建文件")
    parser.add_argument("--port", type=int, default=8000, help="应用运行端口")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细日志")
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    build_app(
        output_dir=args.output, 
        app_name=args.name, 
        clean=not args.no_clean,
        port=args.port
    )