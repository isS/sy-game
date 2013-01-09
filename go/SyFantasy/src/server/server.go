/**
 * Created with IntelliJ IDEA.
 * User: icestar
 * Date: 12-11-11
 * Time: 下午4:02
 * To change this template use File | Settings | File Templates.
 */
package server

import (
	"fmt"
	"net"
	"logger"

	"utils"

)

type Server struct {
	Port 		  string
	ClientVersion int
	TimeoutCount  int
}





func NewServer() *Server {
	logger.Println("init server...")
	server := Server{}
	port,err := utils.Config.GetString("default", "port")
	if err != nil || len(port) <= 0 {
		port = "9080"
	}
	server.Port = port

	version, err := utils.Config.GetInt("default", "clientversion")
	if err != nil {
		version  = 0
	}
	server.ClientVersion = version

	server.TimeoutCount = 0

	return &server
}

func (s *Server) Start() {
	//
	serverAddr := fmt.Sprintf("127.0.0.1:%s", s.Port)
	addr, err := net.ResolveTCPAddr("tcp", serverAddr)
	utils.CheckErr(err)

	listener, err := net.Listen("tcp", addr.String())
	utils.CheckErr(err)

	defer listener.Close()

	id := 0

	logger.Printf("start listen addr %s", serverAddr)

	for {
		client, err := listener.Accept()
		if err != nil {
			utils.CheckErr(err)
			continue
		}

		id++		//增加sessionid

		session := NewSession()   	//新建session
		session.Id = id
		session.Conn = client

		Smgr.Add(session)          //将session添加到sessionmanger

		go session.SessionLoop()
	}

}
