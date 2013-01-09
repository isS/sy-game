/**
 * Created with IntelliJ IDEA.
 * User: icestar
 * Date: 12-11-15
 * Time: 下午12:47
 * To change this template use File | Settings | File Templates.
 */
package server

import (
	"logger"
)


type SessionManager struct {
	sessionMap map[int]*Session
}

var (
	Smgr *SessionManager
)

func init() {
	Smgr = new(SessionManager)
	Smgr.sessionMap = make(map[int]*Session)
}

func (smgr *SessionManager) Add (session *Session) {
	if _, ok := smgr.sessionMap[session.Id]; ok {
		logger.Printf("[smgr add] has same session id (%s)", session.Id)
	} else {
       smgr.sessionMap[session.Id] = session
	}
}

func (smgr *SessionManager) Remove(id int){
	if _, ok := smgr.sessionMap[id]; ok {
		delete(smgr.sessionMap, id)
	} else {
		logger.Printf("[smgr remove] has no session id (%s)", id)
	}
}
