#!/usr/bin/env python3
from operator import truediv
import os

domain=input("输入服务器ip:")
caname=input("请输入ca名（英文）")

def creatca():
    creatcakey="openssl genrsa -out ca.key 4096"
    try:
        os.system(creatcakey)
        print("ca.key文件创建成功")
    except:
        print("创建ca.key文件失败")
    creatcacrt='openssl req -x509 -new -nodes -sha512 -days 36500 -subj "/C=CN/ST=ShangHai/L=ShangHai/O=example/OU=Personal/CN='+caname+'" -key ca.key  -out ca.crt'
    try:
        os.system(creatcacrt)
        print("ca.crt文件创建成功")
    except:
        print("创建ca.crt文件失败")

def creatcsr():
    creatipkey="openssl genrsa -out "+domain+".key 4096"
    try:
        os.system(creatipkey)
        print("ip.key文件创建成功")
    except:
        print("创建ip.key文件失败")
    creatcsr='openssl req -sha512 -new -subj "/C=CN/ST=ShangHai/L=ShangHai/O=example/OU=Personal/CN='+domain+'" -key '+domain+'.key -out '+domain+'.csr'
    try:
        os.system(creatcsr)
        print("ip.csr文件创建成功")
    except:
        print("创建ip.csr文件失败")

def creatv3():
    v3="cat > v3.ext << EOF\nauthorityKeyIdentifier=keyid,issuer\nbasicConstraints=CA:FALSE\nkeyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment\nextendedKeyUsage = serverAuth\nsubjectAltName = @alt_names\n[alt_names]\nDNS.1="+domain+"\nIP.1=127.0.0.1\nIP.2="+domain+"\nEOF"
    try:
        os.system(v3)
        print("配置文件创建成功")
    except:
        print("创建配置文件失败")

def creatcrt():
    crt='openssl x509 -req -sha512 -days 36500 -extfile v3.ext -CA ca.crt -CAkey ca.key -CAcreateserial -in '+domain+'.csr -out '+domain+'.crt'
    try:
        os.system(crt)
        print("crt文件创建成功")
    except:
        print("创建crt文件失败")

ifca=True
ifv3=True
ifcreat=True
if(input("是否需要创建ca文件,若不需要,请将ca.key与ca.crt文件放在运行目录下(Y/n)").lower()=="n"):
    ifca=False
if(input("是否需要创建v3.ext配置文件,若不需要,请将v3.ext文件放在运行目录下(Y/n)").lower()=="n"):
    ifv3=False
if(input("是否需要创建下级证书文件(Y/n)").lower()=="n"):
    ifcreat=False

if(ifca):
    creatca()
if(ifv3):
    creatv3()
if(ifcreat):
    creatcsr()
    creatcrt()