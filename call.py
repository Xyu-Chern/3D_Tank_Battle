# fix_chrome.py - 修复ChromeDriver问题
import os
import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import subprocess
import zipfile
import io

def setup_environment():
    """设置环境变量，使用国内镜像"""
    # 设置国内镜像源
    os.environ['WDM_PROGRESS_BAR'] = '0'
    os.environ['WDM_SSL_VERIFY'] = '0'
    
    # 尝试设置清华镜像（但webdriver-manager可能不支持）
    print("设置环境变量...")
    
def install_webdriver_manager():
    """安装webdriver-manager"""
    print("安装webdriver-manager...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "webdriver-manager", "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])

def download_chromedriver_manual():
    """手动下载ChromeDriver"""
    print("手动下载ChromeDriver...")
    
    # 获取Chrome版本
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
        chrome_version = winreg.QueryValueEx(key, "version")[0]
        major_version = chrome_version.split('.')[0]
        print(f"Chrome版本: {chrome_version}, 主版本: {major_version}")
    except:
        print("无法获取Chrome版本，使用默认版本")
        major_version = "124"  # 假设版本
    
    # 尝试从国内镜像下载
    mirrors = [
        f"https://registry.npmmirror.com/-/binary/chromedriver/{major_version}.0.0.0/",
        f"https://cdn.npmmirror.com/binaries/chromedriver/{major_version}.0.0.0/",
        f"https://chromedriver.storage.googleapis.com/",
    ]
    
    for mirror in mirrors:
        try:
            print(f"尝试镜像: {mirror}")
            # 这里需要实际下载逻辑，但需要知道确切URL
            break
        except:
            continue
    
    return None

def use_firefox_instead():
    """使用Firefox代替Chrome"""
    print("尝试使用Firefox...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.service import Service
        from webdriver_manager.firefox import GeckoDriverManager
        
        # 设置代理或镜像（如果需要）
        import os
        os.environ['WDM_SSL_VERIFY'] = '0'
        
        print("正在下载GeckoDriver...")
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
        print("✓ Firefox启动成功")
        return driver
    except Exception as e:
        print(f"Firefox启动失败: {e}")
        return None

def use_edge_instead():
    """使用Edge浏览器"""
    print("尝试使用Edge...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.edge.service import Service
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service)
        print("✓ Edge启动成功")
        return driver
    except Exception as e:
        print(f"Edge启动失败: {e}")
        return None

def manual_chromedriver_setup():
    """完全手动设置ChromeDriver"""
    print("=" * 60)
    print("手动设置ChromeDriver")
    print("=" * 60)
    
    # 步骤1：检查Chrome版本
    chrome_version = None
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
        chrome_version = winreg.QueryValueEx(key, "version")[0]
        print(f"1. 检测到Chrome版本: {chrome_version}")
    except:
        print("1. 无法自动检测Chrome版本")
        chrome_version = input("请输入你的Chrome版本号（如124.0.6367.91）: ").strip()
    
    # 步骤2：确定主版本号
    if chrome_version:
        major_version = chrome_version.split('.')[0]
        print(f"2. Chrome主版本号: {major_version}")
    else:
        major_version = input("请输入Chrome主版本号（如124）: ").strip()
    
    # 步骤3：提供下载链接
    print("\n3. 请手动下载ChromeDriver:")
    print(f"   下载地址1: https://chromedriver.chromium.org/")
    print(f"   下载地址2: https://registry.npmmirror.com/binary.html?path=chromedriver/")
    print(f"   下载地址3: https://googlechromelabs.github.io/chrome-for-testing/")
    print(f"\n   请下载与Chrome版本 {chrome_version} 匹配的ChromeDriver")
    print(f"   通常下载版本 {major_version}.x.x.x 即可")
    
    # 步骤4：询问是否已下载
    print("\n4. 请将下载的chromedriver.exe放在以下位置之一:")
    print("   - 当前目录 (./chromedriver.exe)")
    print("   - Python安装目录")
    print("   - 系统PATH中的任意目录")
    print("   - 或者告诉我完整路径")
    
    path = input("\n输入chromedriver.exe的完整路径（或直接按回车使用当前目录）: ").strip()
    
    if not path:
        path = "chromedriver.exe"
    
    # 步骤5：验证文件
    if os.path.exists(path):
        print(f"✓ 找到文件: {path}")
        
        # 创建浏览器实例
        try:
            service = Service(path)
            driver = webdriver.Chrome(service=service)
            print("✓ Chrome启动成功！")
            return driver
        except Exception as e:
            print(f"✗ 启动失败: {e}")
            return None
    else:
        print(f"✗ 文件不存在: {path}")
        return None

def try_multiple_browsers():
    """尝试多种浏览器"""
    print("尝试多种浏览器解决方案...")
    
    # 尝试Firefox
    driver = use_firefox_instead()
    if driver:
        return driver
    
    # 尝试Edge
    driver = use_edge_instead()
    if driver:
        return driver
    
    # 手动设置Chrome
    driver = manual_chromedriver_setup()
    if driver:
        return driver
    
    print("所有浏览器尝试都失败了")
    return None

def create_simple_ai_with_current_browser():
    """创建简单的AI控制（使用当前可用的浏览器）"""
    driver = try_multiple_browsers()
    
    if not driver:
        print("无法启动任何浏览器")
        return
    
    print("\n" + "=" * 60)
    print("AI控制系统启动成功！")
    print("=" * 60)
    
    try:
        # 加载游戏
        html_path = os.path.abspath("toy.html")
        file_url = f"file:///{html_path}"
        print(f"加载游戏: {file_url}")
        
        driver.get(file_url)
        time.sleep(3)
        
        # 显示页面信息
        print(f"页面标题: {driver.title}")
        
        # 查找开始按钮
        print("\n查找游戏按钮...")
        buttons = driver.find_elements("tag name", "button")
        print(f"找到 {len(buttons)} 个按钮")
        
        for i, btn in enumerate(buttons[:5]):
            try:
                text = btn.text[:40]
                if text:
                    print(f"  按钮{i+1}: {text}")
            except:
                pass
        
        # 简单AI控制
        print("\n开始简单AI控制...")
        print("按Ctrl+C停止")
        
        # 使用JavaScript控制
        ai_script = """
        // 开始游戏
        function startGame() {
            var buttons = document.getElementsByTagName('button');
            for(var i=0; i<buttons.length; i++) {
                if(buttons[i].innerText.includes('Level 1') || buttons[i].innerText.includes('新手')) {
                    buttons[i].click();
                    return true;
                }
            }
            return false;
        }
        
        // 发送按键
        function sendKey(key) {
            var event = new KeyboardEvent('keydown', {key: key});
            document.dispatchEvent(event);
            setTimeout(() => {
                var event = new KeyboardEvent('keyup', {key: key});
                document.dispatchEvent(event);
            }, 100);
        }
        
        // 开始游戏
        startGame();
        
        // 返回控制函数
        return {
            sendKey: sendKey
        };
        """
        
        # 执行AI脚本
        controller = driver.execute_script(ai_script)
        
        if controller:
            print("✓ 游戏已启动")
            
            # 简单控制循环
            actions = ['w', 'd', 's', 'a', ' ']
            action_names = ['前进', '右转', '后退', '左转', '射击']
            
            for i in range(100):
                try:
                    action_idx = i % len(actions)
                    action = actions[action_idx]
                    action_name = action_names[action_idx]
                    
                    # 发送按键
                    driver.execute_script(f"""
                        var event = new KeyboardEvent('keydown', {{key: '{action}'}});
                        document.dispatchEvent(event);
                        setTimeout(() => {{
                            var event = new KeyboardEvent('keyup', {{key: '{action}'}});
                            document.dispatchEvent(event);
                        }}, 200);
                    """)
                    
                    print(f"动作 {i+1}: {action_name}")
                    
                    # 偶尔射击
                    if i % 4 == 0 and action != ' ':
                        driver.execute_script("""
                            var event = new KeyboardEvent('keydown', {key: ' '});
                            document.dispatchEvent(event);
                            setTimeout(() => {
                                var event = new KeyboardEvent('keyup', {key: ' '});
                                document.dispatchEvent(event);
                            }, 100);
                        """)
                        print("  射击")
                    
                    time.sleep(0.5)
                    
                except KeyboardInterrupt:
                    print("\n用户中断")
                    break
                except Exception as e:
                    print(f"控制错误: {e}")
                    time.sleep(1)
        
        else:
            print("✗ 无法启动游戏")
        
        print("\nAI控制结束")
        
    except Exception as e:
        print(f"程序错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        input("\n按回车键关闭浏览器...")
        driver.quit()

def offline_solution():
    """离线解决方案：使用已安装的ChromeDriver"""
    print("=" * 60)
    print("离线解决方案")
    print("=" * 60)
    
    # 检查常见位置的ChromeDriver
    common_paths = [
        "chromedriver.exe",  # 当前目录
        "chromedriver/chromedriver.exe",
        "drivers/chromedriver.exe",
        "C:/Windows/System32/chromedriver.exe",
        "C:/Program Files/chromedriver/chromedriver.exe",
        os.path.join(os.environ.get('USERPROFILE', ''), "Downloads/chromedriver.exe"),
        os.path.join(os.environ.get('USERPROFILE', ''), "Desktop/chromedriver.exe"),
    ]
    
    print("搜索ChromeDriver...")
    found_path = None
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"✓ 找到: {path}")
            found_path = path
            break
    
    if not found_path:
        print("未找到ChromeDriver")
        print("\n请手动下载ChromeDriver:")
        print("1. 查看Chrome版本: chrome://settings/help")
        print("2. 下载地址: https://chromedriver.chromium.org/")
        print("3. 下载对应版本，解压后将chromedriver.exe放在当前目录")
        
        # 检查是否有旧版本Selenium可以使用
        try:
            print("\n尝试使用旧版本Selenium...")
            # 尝试直接使用系统PATH中的ChromeDriver
            from selenium import webdriver
            driver = webdriver.Chrome()
            return driver
        except:
            pass
        
        return None
    
    # 使用找到的路径
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        
        service = Service(found_path)
        driver = webdriver.Chrome(service=service)
        print("✓ Chrome启动成功")
        return driver
    except Exception as e:
        print(f"启动失败: {e}")
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("坦克大战AI控制系统 - 浏览器修复版")
    print("=" * 60)
    
    # 检查是否有HTML文件
    if not os.path.exists("toy.html"):
        print("✗ 错误: 未找到 toy.html 文件")
        print("请将游戏文件放在当前目录")
        input("按回车键退出...")
        return
    
    print("选择解决方案:")
    print("1. 自动尝试多种浏览器")
    print("2. 手动设置ChromeDriver")
    print("3. 离线搜索已安装的ChromeDriver")
    print("4. 退出")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    driver = None
    
    try:
        if choice == '1':
            print("\n正在尝试多种浏览器...")
            driver = try_multiple_browsers()
            
        elif choice == '2':
            print("\n手动设置ChromeDriver...")
            driver = manual_chromedriver_setup()
            
        elif choice == '3':
            print("\n离线搜索...")
            driver = offline_solution()
            
        else:
            print("退出")
            return
        
        if driver:
            # 运行AI控制
            create_simple_ai_with_current_browser()
        else:
            print("\n无法启动浏览器，请尝试:")
            print("1. 安装Firefox浏览器")
            print("2. 手动下载ChromeDriver并放在当前目录")
            print("3. 使用系统自带的Edge浏览器")
            
    except Exception as e:
        print(f"程序错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
    
    input("\n按回车键退出程序...")

if __name__ == "__main__":
    # 确保必要的包已安装
    try:
        from selenium import webdriver
    except ImportError:
        print("安装selenium...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
    
    main()