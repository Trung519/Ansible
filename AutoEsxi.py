#!/usr/bin/env python3
"""
Script test kết nối ESXi với SSL self-signed certificate
"""

from pyVim.connect import SmartConnect, Disconnect
import ssl
import urllib3
import warnings

# Tắt tất cả SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

# Thông tin ESXi
ESXI_HOST = "192.168.241.135"
ESXI_USER = "root"
ESXI_PASS = "qtrung@123"
ESXI_PORT = 443

def test_esxi_connection():
    """Test kết nối ESXi với các phương pháp khác nhau"""
    
    print("🔐 Test kết nối ESXi với self-signed SSL certificate")
    print(f"Host: {ESXI_HOST}:{ESXI_PORT}")
    print("=" * 60)
    
    # Phương pháp: SSL context + disableSslCertValidation
    print("\n Thử kết nối với SSL context + disableSslCertValidation...")
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        si = SmartConnect(
            host=ESXI_HOST,
            user=ESXI_USER,
            pwd=ESXI_PASS,
            port=ESXI_PORT,
            sslContext=context,
            disableSslCertValidation=True
        )
        
        content = si.RetrieveContent()
        print(f"✅ Kết nối thành công!")
        print(f"   ESXi Version: {content.about.version}")
        print(f"   Build: {content.about.build}")
        print(f"   Full Name: {content.about.fullName}")
        
        Disconnect(si)
        return True
        
    except Exception as e:
        print(f"❌ Thất bại: {e}")

def check_esxi_certificate():
    """Kiểm tra certificate của ESXi"""
    print("\n🔍 Kiểm tra SSL Certificate...")
    
    import socket
    
    try:
        # Tạo kết nối socket
        sock = socket.create_connection((ESXI_HOST, ESXI_PORT), timeout=10)
        
        # Wrap với SSL
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with context.wrap_socket(sock, server_hostname=ESXI_HOST) as ssock:
            cert = ssock.getpeercert()
            print(f"✅ SSL handshake thành công")
            
            if cert:
                print(f"   Subject: {cert.get('subject', 'N/A')}")
                print(f"   Issuer: {cert.get('issuer', 'N/A')}")
                print(f"   Version: {cert.get('version', 'N/A')}")
            else:
                print("   Certificate info: Không có (self-signed)")
                
    except Exception as e:
        print(f"❌ SSL handshake thất bại: {e}")

def main():
    # Test kết nối
    success = test_esxi_connection()
    
    # Kiểm tra certificate
    check_esxi_certificate()
    
    print("\n" + "="*60)
    if success:
        print("🎉 Kết nối ESXi thành công! Có thể chạy script tạo VM.")
    else:
        print("❌ Tất cả phương pháp kết nối đều thất bại.")

if __name__ == "__main__":
    main()
