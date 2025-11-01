# ============================================================================
# notification.py - 邮件通知模块（真实发送版本）
# ============================================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_email(subject, body, to_email, from_email, password):
    """
    发送真实邮件

    参数:
    subject: 邮件主题
    body: 邮件正文
    to_email: 收件人邮箱
    from_email: 发件人邮箱（Gmail）
    password: Gmail 应用专用密码（16位）

    返回:
    bool: 成功返回 True，失败返回 False
    """

    try:
        # 创建邮件
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # 连接 Gmail SMTP 服务器
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # 登录
        server.login(from_email, password)

        # 发送
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()

        print(f"✅ 邮件发送成功！")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f"❌ 登录失败：邮箱或密码错误")
        print(f"💡 确保使用应用专用密码，不是登录密码")
        return False

    except Exception as e:
        print(f"❌ 发送失败：{e}")
        return False


def send_trading_signal(symbol, signal, price_info, to_email, from_email, password):
    """
    发送交易信号邮件

    参数:
    symbol: 股票代码
    signal: 交易信号（BUY/SELL/HOLD）
    price_info: 价格信息字典 {'current': 价格, 'high_20': 最高, 'low_10': 最低}
    to_email: 收件人邮箱
    from_email: 发件人邮箱
    password: 应用专用密码

    返回:
    bool: 成功返回 True
    """

    # 根据信号设置内容
    signal_config = {
        "BUY": {"emoji": "🟢", "action": "买入", "desc": "价格突破20日最高点"},
        "SELL": {"emoji": "🔴", "action": "卖出", "desc": "价格跌破10日最低点"},
        "HOLD": {"emoji": "🟡", "action": "持有", "desc": "价格在通道内"}
    }

    config = signal_config.get(signal, signal_config["HOLD"])

    # 邮件主题
    subject = f"{config['emoji']} 海龟法则提醒：{symbol} - {config['action']}信号"

    # 邮件正文
    current = price_info.get('current', 0)
    high_20 = price_info.get('high_20', 0)
    low_10 = price_info.get('low_10', 0)

    body = f"""
🐢 海龟法则交易提醒
{'=' * 50}

📊 股票信息
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
股票代码：{symbol}
当前价格：${current:.2f}

📈 技术指标
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
20日最高价：${high_20:.2f}
10日最低价：${low_10:.2f}

🎯 交易信号
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
信号：{signal} ({config['action']})
说明：{config['desc']}

⏰ 分析时间
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

{'=' * 50}

💡 建议操作：{config['action']}该股票

⚠️  风险提示：
本提醒基于技术分析，仅供参考。
投资有风险，决策需谨慎。

{'=' * 50}
海龟法则自动提醒系统 v1.0
    """

    return send_email(subject, body, to_email, from_email, password)


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("📧 邮件通知模块测试")
    print("=" * 60)

    # ⚠️ 配置区域 - 请修改为你的信息
    FROM_EMAIL = "lareina6145@gmail.com"
    TO_EMAIL = "lareina6145@gmail.com"
    APP_PASSWORD = "jyzwmckgordxikab"

    print(f"\n当前配置：")
    print(f"发件人: {FROM_EMAIL}")
    print(f"收件人: {TO_EMAIL}")

    # 检查配置
    if FROM_EMAIL == "your_email@gmail.com":
        print(f"\n⚠️  请先配置邮箱信息！")
        print(f"\n📝 配置步骤：")
        print(f"1. 开启 Gmail 两步验证")
        print(f"   https://myaccount.google.com/security")
        print(f"\n2. 生成应用专用密码")
        print(f"   https://myaccount.google.com/apppasswords")
        print(f"\n3. 在上方修改配置：")
        print(f"   FROM_EMAIL = '你的邮箱@gmail.com'")
        print(f"   TO_EMAIL = '收件邮箱@gmail.com'")
        print(f"   APP_PASSWORD = '16位应用密码（无空格）'")
    else:
        # 开始测试
        print(f"\n✅ 配置已填写，开始测试...")

        # 测试1：简单邮件
        print(f"\n🧪 测试1：发送测试邮件")
        print("-" * 60)

        success = send_email(
            subject="海龟法则系统 - 测试邮件",
            body="恭喜！邮件功能配置成功！\n\n这是一封测试邮件。",
            to_email=TO_EMAIL,
            from_email=FROM_EMAIL,
            password=APP_PASSWORD
        )

        if success:
            print(f"\n✅ 测试成功！")
            print(f"💡 请检查邮箱：{TO_EMAIL}")
            print(f"   （可能在垃圾邮件中）")

            # 测试2：交易信号
            print(f"\n🧪 测试2：发送交易信号")
            print("-" * 60)

            price_info = {
                'current': 255.50,
                'high_20': 254.00,
                'low_10': 240.00
            }

            success2 = send_trading_signal(
                symbol="AAPL",
                signal="BUY",
                price_info=price_info,
                to_email=TO_EMAIL,
                from_email=FROM_EMAIL,
                password=APP_PASSWORD
            )

            if success2:
                print(f"\n🎉 所有测试通过！")
                print(f"📧 邮件功能配置完成！")
        else:
            print(f"\n❌ 测试失败")
            print(f"\n🔧 故障排查：")
            print(f"1. 检查邮箱地址是否正确")
            print(f"2. 确认使用应用专用密码（不是登录密码）")
            print(f"3. 检查密码是否去掉了所有空格")
            print(f"4. 确认两步验证已开启")