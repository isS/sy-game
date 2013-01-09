/**
 * Created with IntelliJ IDEA.
 * User: icestar
 * Date: 12-11-11
 * Time: 下午4:29
 * To change this template use File | Settings | File Templates.
 */
package server

import (
	"net"
//	"io"
	"bufio"

	"logger"
	"utils"

)

const (
	BUFFER_MAXSIZE = 16384
)

type Session struct {
	Id 			int
	Conn 		net.Conn
}

func NewSession() *Session {
	session := new(Session)

	return session
}

/*
session 循环
 */
func (session *Session) SessionLoop() {
	defer session.Conn.Close()
	//处理连接建立
	session.CreateConnection()

	for {
		//从socket接受数据
		data, err := bufio.NewReader(session.Conn).ReadString('\n');

		if err != nil {
			utils.CheckErr(err)
			Smgr.Remove(session.Id)     //移除sesssion
			session.Disconnected()     	//链接断开
			break

		}
		data = data[0:len(data) - 1]      //去除最后的换行字符
		session.HandleReceive(data)
	}


}

/**
建立连接
 */
func (session *Session) CreateConnection() {
   logger.Printf("[%s][connect] %s ", session.Id, session.Conn.RemoteAddr())
}

/**
断开连接
 */
func (session *Session) Disconnected() {
	logger.Printf("[%d][disconnect] %s", session.Id, session.Conn.RemoteAddr())
}

/*
处理来自客户端的数据
 */
func (session *Session) HandleReceive(data string ){
	logger.Printf("[%d][reveive %d] %s ",session.Id, len(data), data)











}

/**
解析接口
 */
func (session *Session) ParseAction(p *Packet){

}


