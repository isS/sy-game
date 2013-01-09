/**
 * Created with IntelliJ IDEA.
 * User: icestar
 * Date: 12-11-14
 * Time: 下午10:01
 * To change this template use File | Settings | File Templates.
 */
package utils

import (
	"logger"
)



func CheckErr(err error) {
	if err != nil {
		logger.Printf("Fatal error: %s", err.Error())

		//os.Exit(1)
	}
}
