import unittest
import subprocess
import os
import time
from pathlib import Path
import winreg
try:
    import psutil
except ImportError:
    print("请先安装psutil: pip install psutil")
    psutil = None
import shutil

class TestFullInstallation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if psutil is None:
            raise unittest.SkipTest("psutil未安装")
            
        cls.app_name = "AI文章生成助手"
        cls.install_path = Path(r"C:\Program Files\AI文章生成助手")
        cls.start_menu_path = Path(os.environ["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs/AI文章生成助手"
        
    def test_01_installation(self):
        """测试安装过程"""
        installer = Path("release/installer/AI文章生成助手_安装程序_v0.1.0.exe")
        self.assertTrue(installer.exists(), "安装程序不存在")
        
        # 运行安装程序
        result = subprocess.run([str(installer), "/SILENT", "/SUPPRESSMSGBOXES"], capture_output=True)
        self.assertEqual(result.returncode, 0, "安装程序执行失败")
        
        # 检查安装目录
        self.assertTrue(self.install_path.exists(), "程序未正确安装")
        self.assertTrue((self.install_path / "AI文章生成助手.exe").exists(), "主程序不存在")
        
    def test_02_shortcuts(self):
        """测试快捷方式创建"""
        # 检查开始菜单快捷方式
        start_menu_shortcut = self.start_menu_path / "AI文章生成助手.lnk"
        self.assertTrue(start_menu_shortcut.exists(), "开始菜单快捷方式未创建")
        
        # 检查桌面快捷方式
        desktop_path = Path(os.path.expanduser("~/Desktop"))
        desktop_shortcut = desktop_path / "AI文章生成助手.lnk"
        if desktop_shortcut.exists():  # 桌面快捷方式是可选的
            self.assertTrue(desktop_shortcut.is_file())
            
    def test_03_program_launch(self):
        """测试程序启动"""
        exe_path = self.install_path / "AI文章生成助手.exe"
        
        # 启动程序
        process = subprocess.Popen([str(exe_path)])
        time.sleep(5)  # 等待程序完全启动
        
        # 检查进程是否在运行
        self.assertIsNone(process.poll(), "程序未能保持运行")
        
        # 检查是否有主窗口
        def find_window():
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == 'AI文章生成助手.exe':
                    return True
            return False
            
        self.assertTrue(find_window(), "未找到程序主窗口")
        
        # 关闭程序
        process.terminate()
        process.wait()
        
    def test_04_model_loading(self):
        """测试模型加载"""
        # 检查模型文件
        model_path = self.install_path / "models"
        self.assertTrue(model_path.exists(), "模型目录不存在")
        
        # 检查是否有模型文件
        model_files = list(model_path.glob("*"))
        self.assertGreater(len(model_files), 0, "模型文件未下载")
        
    def test_05_file_processing(self):
        """测试文件处理功能"""
        # 创建测试文件
        test_file = Path("test_input.txt")
        test_content = "这是一个测试文本，用于验证文件处理功能。"
        test_file.write_text(test_content, encoding='utf-8')
        
        try:
            # 启动程序并处理文件
            exe_path = self.install_path / "AI文章生成助手.exe"
            process = subprocess.Popen([str(exe_path), str(test_file)])
            time.sleep(5)
            
            # 检查输出目录
            output_dir = self.install_path / "output"
            self.assertTrue(output_dir.exists(), "输出目录不存在")
            
            # 检查是否生成了输出文件
            output_files = list(output_dir.glob("*"))
            self.assertGreater(len(output_files), 0, "未生成输出文件")
            
        finally:
            # 清理
            if test_file.exists():
                test_file.unlink()
            if process.poll() is None:
                process.terminate()
                process.wait()
                
    def test_06_uninstall(self):
        """测试卸载过程"""
        uninstaller = self.install_path / "unins000.exe"
        self.assertTrue(uninstaller.exists(), "卸载程序不存在")
        
        # 运行卸载程序
        result = subprocess.run([str(uninstaller), "/SILENT", "/SUPPRESSMSGBOXES"], capture_output=True)
        self.assertEqual(result.returncode, 0, "卸载程序执行失败")
        
        # 等待卸载完成
        time.sleep(5)
        
        # 检查文件清理
        self.assertFalse(self.install_path.exists(), "程序目录未完全删除")
        self.assertFalse(self.start_menu_path.exists(), "开始菜单项未删除")
        
        # 检查注册表清理
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\AI文章生成助手")
            self.fail("注册表项未清理")
        except WindowsError:
            pass  # 预期行为：注册表项应该不存在

def run_tests():
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFullInstallation)
    
    # 运行测试并生成报告
    with open('installation_test_report.txt', 'w', encoding='utf-8') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = runner.run(suite)
        
        # 添加总结
        f.write("\n=== 测试总结 ===\n")
        f.write(f"运行测试数: {result.testsRun}\n")
        f.write(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}\n")
        f.write(f"失败: {len(result.failures)}\n")
        f.write(f"错误: {len(result.errors)}\n")

if __name__ == '__main__':
    run_tests() 