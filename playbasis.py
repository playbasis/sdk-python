import requests, json

class Playbasis:
    """The Playbasis Object"""
    
    BASE_URL = 'https://api.pbapp.net/'
    BASE_ASYNC_URL = 'https://api.pbapp.net/async/';

    def __init__(self):
        self.token = None
        self.apiKeyParam = None
        self.respChannel = None

    def auth(self, apiKey, apiSecret):
        self.apiKeyParam = '?api_key=' + apiKey
        result = self.call('Auth', {'api_key': apiKey,
                                     'api_secret': apiSecret})
        self.token = result['response']['token']
        return isinstance(self.token, basestring)

    def renew(self, apiKey, apiSecret):
        self.apiKeyParam = '?api_key=' + apiKey
        result = self.call('Auth/renew', {'api_key': apiKey,
                                     'api_secret': apiSecret})
        self.token = result['response']['token']
        return isinstance(self.token, basestring)

    def setAsyncResponseChannel(self, channel):
        url = self.BASE_ASYNC_URL + 'channel/verify/' + channel

        res = requests.get(url, verify=False).text.strip()

        if res == "true":
            self.respChannel = channel
            return True
        return False

    def player(self, playerId):
        return self.call('Player/' + playerId, {'token': self.token})

    # playerListId player id as used in client's website separate with ',' example '1,2,3'
    def playerList(self, playerListId):
        return self.call('Player/list', {'token': self.token, 'list_player_id': playerListId})

    def playerDetail(self, playerId):
        return self.call('Player/' + playerId + '/data/all', {'token': self.token})

    # @param    optionalData    Key-value for additional parameters to be sent to the register method.
    #                           The following keys are supported:
    #                           - facebook_id
    #                           - twitter_id
    #                           - password      assumed hashed
    #                           - first_name
    #                           - last_name
    #                           - nickname
    #                           - gender        1=Male, 2=Female
    #                           - birth_date    format YYYY-MM-DD
    def register(self, playerId, username, email, imageUrl, optionalData={}):
        data = {
            'token' : self.token,
            'username' : username,
            'email' : email,
            'image' : imageUrl
        }
        data.update(optionalData)
        return self.call('Player/' + playerId + '/register', data)

    def registerAsync(self, playerId, username, email, imageUrl, optionalData={}):
        data = {
            'token' : self.token,
            'username' : username,
            'email' : email,
            'image' : imageUrl
        }
        data.update(optionalData)
        return self.callAsync('Player/' + playerId + '/register', data, self.respChannel)

    #   @param	updateData		Key-value for data to be updated.
    # 							The following keys are supported:
    #							- username
    #							- email
    #							- image
    #							- exp
    #							- level
    # 							- facebook_id
    # 							- twitter_id
    # 							- password		assumed hashed
    # 							- first_name
    # 							- last_name
    # 							- nickname
    # 							- gender		1=Male, 2=Female
    # 							- birth_date	format YYYY-MM-DD
    def update(self, playerId, updateData={}):
        data = {
            'token': self.token
        }
        data.update(updateData)
        return self.call('Player/' + playerId + '/update', data)

    def updateAsync(self, playerId, updateData={}):
        data = {
            'token': self.token
        }
        data.update(updateData)
        return self.callAsync('Player/' + playerId + '/update', data, self.respChannel)

    def delete(self, playerId):
        return self.call('Player/' + playerId + '/delete', {'token': self.token})

    def deleteAsync(self, playerId):
        return self.callAsync('Player/' + playerId + '/delete', {'token': self.token}, self.respChannel)

    def login(self, playerId):
        return self.call('Player/' + playerId + '/login', {'token': self.token})

    def loginAsync(self, playerId):
        return self.callAsync('Player/' + playerId + '/login', {'token': self.token}, self.respChannel)

    def logout(self, playerId):
        return self.call('Player/' + playerId + '/logout', {'token': self.token})

    def logoutAsync(self, playerId):
        return self.callAsync('Player/' + playerId + '/logout', {'token': self.token}, self.respChannel)

    def points(self, playerId):
        return self.call('Player/%s/points%s' % (playerId, self.apiKeyParam))

    def point(self, playerId, pointName):
        return self.call('Player/%s/point/%s%s' % (playerId, pointName, self.apiKeyParam))

    def pointHistory(self, playerId, pointName='', offset=0, limit=20):
        string_query = '&offset=%s&limit=%s' % (offset, limit)
        if pointName != '':
            string_query = '%s&point_name=%s' % (string_query, pointName)
        return self.call('Player/%s/point_history%s%s' % (playerId, self.apiKeyParam, string_query))

    def actionLastPerformed(self, playerId):
        return self.call('Player/%s/action/time%s' % (playerId, self.apiKeyParam))
    
    def actionLastPerformedTime(self, playerId, actionName):
        return self.call('Player/%s/action/%s/time%s' % (playerId, actionName, self.apiKeyParam))
    
    def actionPerformedCount(self, playerId, actionName):
        return self.call('Player/%s/action/%s/count%s' % (playerId, actionName, self.apiKeyParam))
    
    def badgeOwned(self, playerId):
        return self.call('Player/%s/badge%s' % (playerId, self.apiKeyParam))
    
    def rank(self, rankedBy, limit=20):
        return self.call('Player/rank/%s/%s%s' % (rankedBy, limit, self.apiKeyParam))

    def ranks(self, limit=20):
        return self.call('Player/ranks/%s%s' % (limit, self.apiKeyParam))

    def levels(self):
        return self.call('Player/levels%s' % self.apiKeyParam)

    def level(self, level):
        return self.call('Player/level/%s%s' % (level, self.apiKeyParam))

    def claimBadge(self, playerId, badgeId):
        return self.call('Player/%s/badge/%s/claim' % (playerId, badgeId), {'token': self.token})

    def redeemBadge(self, playerId, badgeId):
        return self.call('Player/%s/badge/%s/redeem' % (playerId, badgeId), {'token': self.token})

    def goodsOwned(self, playerId):
        return self.call('Player/%s/goods%s' % (playerId, self.apiKeyParam))

    def questOfPlayer(self, playerId, questId):
        return self.call('Player/quest/%s%s&player_id=%s' % (questId, self.apiKeyParam, playerId))

    def questListOfPlayer(self, playerId):
        return self.call('Player/quest%s&player_id=%s' % (self.apiKeyParam, playerId))

    def badges(self):
        return self.call('Badge' + self.apiKeyParam)
    
    def badge(self, badgeId):
        return self.call('Badge/' + badgeId + self.apiKeyParam)

    def goodsList(self):
        return self.call('Goods%s' % self.apiKeyParam)

    def goods(self, goodsId):
        return self.call('Goods/%s%s' % (goodsId, self.apiKeyParam))

    def actionConfig(self):
        return self.call('Engine/actionConfig' + self.apiKeyParam)

    # @param    optionalData    Key-value for additional parameters to be sent to the rule method.
    #                           The following keys are supported:
    #                           - url       url or filter string (for triggering non-global actions)
    #                           - reward    name of the custom-point reward to give (for triggering rules with custom-point reward)
    #                           - quantity  amount of points to give (for triggering rules with custom-point reward)
    def rule(self, playerId, action, optionalData={}):
        data = {
            'token' : self.token,
            'player_id' : playerId,
            'action' : action
        }
        data.update(optionalData)
        return self.call('Engine/rule', data)

    def ruleAsync(self, playerId, action, optionalData={}):
        data = {
            'token' : self.token,
            'player_id' : playerId,
            'action' : action
        }
        data.update(optionalData)
        return self.callAsync('Engine/rule', data, self.respChannel)

    def quests(self):
        return self.call('Quest%s' % self.apiKeyParam)

    def quest(self, questId):
        return self.call('Quest/%s%s' % (questId, self.apiKeyParam))

    def mission(self, questId, missionId):
        return self.call('Quest/%s/misson/%s%s' % (questId, missionId, self.apiKeyParam))

    def questsAvailable(self, playerId):
        return self.call('Quest/available%s&player_id=%s' % (self.apiKeyParam, playerId))

    def questAvailable(self, questId, playerId):
        return self.call('Quest/%s/available/%s&player_id=%s' % (questId, self.apiKeyParam, playerId))

    def joinQuest(self, questId, playerId):
        data = {
            'token': self.token,
            'player_id': playerId
        }
        return self.call('Quest/%s/join' % questId, data)

    def joinQuestAsync(self, questId, playerId):
        data = {
            'token': self.token,
            'player_id': playerId
        }
        return self.callAsync('Quest/%s/join' % questId, data, self.respChannel)

    def cancelQuest(self, questId, playerId):
        data = {
            'token': self.token,
            'player_id': playerId
        }
        return self.call('Quest/%s/cancel' % questId, data)

    def cancelQuestAsync(self, questId, playerId):
        data = {
            'token': self.token,
            'player_id': playerId
        }
        return self.callAsync('Quest/%s/cancel' % questId, data, self.respChannel)

    def redeemGoods(self, goodsId, playerId, amount=1):
        data = {
            'token': self.token,
            'goods_id': goodsId,
            'player_id': playerId,
            'amount': amount,
        }
        return self.call('Redeem/goods', data)

    def redeemGoodsAsync(self, goodsId, playerId, amount=1):
        data = {
            'token': self.token,
            'goods_id': goodsId,
            'player_id': playerId,
            'amount': amount,
        }
        return self.callAsync('Redeem/goods', data, self.respChannel)

    def recentPoint(self, offset=0, limit=10):
        return self.call('Service/recent_point%s&offset=%s&limit=%s' % (self.apiKeyParam, offset, limit))

    def recentPointByName(self, pointName, offset=0, limit=10):
        return self.call('Service/recent_point%s&offset=%s&limit=%s&point_name=%s' % (self.apiKeyParam, offset, limit, pointName))

    def call(self, method, data=None):
        url = self.BASE_URL + method
        print 'requesting url: ' + url
        if data:
            return json.loads(requests.post(url, data, verify=False).text)
        return json.loads(requests.get(url, verify=False).text)

    def callAsync(self, method, data=None, responseChannel=None):
        url = self.BASE_ASYNC_URL + 'call'
        print 'requesting url: ' + url
        if data:
            body = []
            body['endpoint'] = method
            body['data'] = data
            if responseChannel:
                body['channel'] = responseChannel
            body = json.loads(body)
            return json.loads(requests.post(url, body, verify=False).text)
        return json.loads(requests.get(url, verify=False).text)