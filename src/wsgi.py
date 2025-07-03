# 預載資源
preload_app = True

# 綁定
bind = "0.0.0.0:5555"

# 進程數
# - 設為1 保持ws session，高迸發量則建議設為 python3 -c 'import multiprocessing as mp; print(mp.cpu_count()*2 + 1)'
workers = 3

# 線程數
threads = 5

# 等待隊列最大長度,超過這個長度的鏈接將被拒絕連接
backlog = 1024

# 工作模式
worker_class = "gevent"

# 最大客戶客戶端併發數量,對使用線程和協程的worker的工作有影響
worker_connections = 1024

# 日誌設定
# - 記錄等級
loglevel = 'info'
# - 錯誤記錄
errorlog = '-'
# - 操作記錄
accesslog = '-'
# - Format e.g. [08/Dec/2021:20:32:10 +0800] [200] [5.192.194.57] "GET /info?id=2 HTTP/1.1 PostmanRuntime/7.28.4"
access_log_format = '%(t)s [%(s)s] [%({x-real-ip}i)s] "%(r)s %(a)s"'
