#coding=utf-8
__author__ = 'icestar'

import json

class SkinManager:

    def __init__(self):
        self.skins = {}

    def loadSkins(self):
        with open("./res/skins.json", "r") as fp:
            self.skins = json.load(fp)

    def get_skin(self, name):
        if self.skins.has_key(name):
            return self.skins[name]
        else:
            raise "[skin] 不能找到该skin"


Instance = SkinManager()
Instance.loadSkins()