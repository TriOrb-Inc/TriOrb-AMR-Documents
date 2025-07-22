# Package: triorb_sls_drive_manager

## SLS(sick社製)のサンプルモジュール

## Subscriber
### Description
- Topic: /drive/std_vector
- Type: Float32MultiArray
- Usage: 進行方向のSLSのセンシング範囲を決める

### setup
- Ethernet通信 : サービスとして登録
- 進行方向の取得 : triorb_drive_vector
### install
```bash
sudo bash ./setup.bash
```