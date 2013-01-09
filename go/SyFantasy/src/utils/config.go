/**
 * Created with IntelliJ IDEA.
 * User: icestar
 * Date: 12-11-14
 * Time: 下午10:05
 * To change this template use File | Settings | File Templates.
 */
package utils
import (
	"conf"
)

var (
	Config *conf.ConfigFile
)

func init() {
	c, err := conf.ReadConfigFile("data/server.conf")
	CheckErr(err)
	Config = c
}

func GetString(section string, option string) (value string, err error){
	return Config.GetString(section, option)
}

