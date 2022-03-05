## Confuse(2022/3/4)
### ubuntu
1. **sudo apt update && sudo apt upgrade**
	- [跟新](https://project.zhps.tp.edu.tw/ethan/2019/03/ubuntu-%E6%9B%B4%E6%96%B0%E8%88%87%E5%8D%87%E7%B4%9A/)
2. **rsync / scp**
	- rsync -ravz --progress -e 
	- rsync -ravz --progress -e "ssh  -i aws-test.pem" [遠端機器] :~/
3. **vim**
	- [vim使用](https://zhuanlan.zhihu.com/p/68111471)
4. **git**
	 - sudo apt-get install git
	 - git clone [url]
	 - git checkout [branch]
5. **mysql**
	- [安裝](https://ubunlog.com/zh-TW/MySQL-8-Ubuntu%E6%95%B8%E6%93%9A%E5%BA%AB/)
	- [初始設定](https://www.albert-yu.com/blog/mysql%E8%A8%AD%E5%AE%9Aroot%E5%B8%B3%E8%99%9F%E5%AF%86%E7%A2%BC%E8%88%87%E5%88%9D%E5%A7%8B%E6%AC%8A%E9%99%90ubuntu-20-04/)
	- [mysqldump編碼問題](https://blog.csdn.net/ycf8788/article/details/101035640)
6. **安裝python**
	- [安裝3.10 > 跟新指令 > 切換版本](https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-10-on-ubuntu-18-04-and-20-04-lts/)
	- [安裝pip](https://linuxize.com/post/how-to-install-pip-on-ubuntu-20.04/)

### ubuntu error
1. **sudo apt update && sudo apt upgrade**
	- [NO_PUBKEY](https://blog.wu-boy.com/2012/05/how-to-resolve-apt-get-no_pubkey-gpg-error/)
	- [apt_pkg](ModuleNotFoundError: No module named 'apt_pkg' error)

### python
- **code**
	- [ ] 1. 巢狀資料結構(處理)
		- for loop / pandas / (else...)
	- [x] 2. (json > mysql) or (json > csv > mysql)
		- [json > mysql](https://segmentfault.com/a/1190000024445924)
		- 不確定,得再查資料
	- [ ] 3. mysql 取出資料 > 處理成json格式
		- sql > json
		- sql > python(dict&list) > json
	- [ ] 4. %, {}.format, ... (占位符/格式化/...)
- **mysql**
	- [ ] 1. connection pool
		- 了解(python)如何實現連接池
	- [ ] 2. json儲存問題(資料型態) 
		- 直接存 / 轉成表格
		- 編碼問題
	- [ ] 3. 資料表設計
		- 何時要分表?
	- [ ] 4. sql語句(優化)
- **flask**
	- [ ] 1. status code
	- [ ] 2. api 返回 json 概念
		- jsonify / json.dumps / 自訂Response，使用force_type()
	- [ ] 3. retutn 什麼 / Response
		- 前後端串接
	- [ ] 4. cookie, session, token, jwt, oauth2
***
### javascript
- [ ] 1. ajax / fetch
- [ ] 2. fetch(get / post)取值
- [ ] 3. Content-Type
- [ ] 4. 箭頭函式

