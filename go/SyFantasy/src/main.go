/**
 * Created with IntelliJ IDEA.
 * User: icestar
 * Date: 12-11-6
 * Time: 上午10:10
 * To change this template use File | Settings | File Templates.
 */
package main

import (
	"flag"
	"fmt"
	"runtime"
	"database/sql"

	"logger"
	_ "pq"
	"beedb"

	"utils"
	"server"

)


var (
	//configFile *string = flag.String("config", "server.conf", "需要加载的配置文件名字")
)


func main() {
	flag.Parse()

	// Always use the maximum available CPU/Cores
	runtime.GOMAXPROCS(runtime.NumCPU())

	if !initLogger() {
		return
	}

	if !initDatabases() {
		return
	}

	gameServer := server.NewServer()
	gameServer.Start()

}





func initLogger() bool {
	var flags int

	toConsole, err := utils.Config.GetBool("log", "console")
	if err != nil || toConsole {
		flags = logger.L_CONSOLE
	}

	toFile, err := utils.Config.GetBool("log", "file")
	if err != nil || toFile {
		flags = flags | logger.L_FILE
	}

	logFile, err := utils.Config.GetString("log", "filename")
	if err != nil || len(logFile) <= 0 {
		logFile = "log.txt"
	}

	logger.LogFilename = logFile
	logger.Flags = flags

	result := logger.Init()
	if !result {
		logger.Println("logger init faild")
	}

	return result

}

func initDatabases() bool {
//	dbHost := gConfig.GetString("database", "host")
//	dbPort := gConfig.getString("database", "port")
	user, _ := utils.Config.GetString("database", "user")
	pwd, _ := utils.Config.GetString("database", "password")
	dbname, _ := utils.Config.GetString("database", "db")


	dataSourceName := fmt.Sprintf("user=%s password=%s dbname=%s sslmode=disable", user, pwd, dbname)
	db, err := sql.Open("postgres", dataSourceName )
	utils.CheckErr(err)

	beedb.New(db, "pq")
	return true
}
