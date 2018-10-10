# 环境：
python 2.7
salt 2018.3
MySQL 5.5+

#使用方法

1.将ex_models里面的文件放到你的file_root目录里
然后salt '*' saltutil.sync_modules推送到各个节点

2.定时任务（确保各个主机的状态）
*/5 * * * * /usr/bin/curl http://IP:Port/server/status/ >2&1>>/dev/null
