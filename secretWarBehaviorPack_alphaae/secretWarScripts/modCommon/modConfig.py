# -*- coding: utf-8 -*-
# 这个文件保存了MOD中使用的一些变量，这样做的好处很多，建议参考

# Mod Version
ModName = "SecretWarAddon"
ModVersion = "0.0.1"

# Server System
ServerSystemName = "MainServerSystem"
ServerSystemClsPath = "secretWarScripts.modServer.serverSystem.mainServerSystem.MainServerSystem"

# Client System
ClientSystemName = "MainClientSystem"
ClientSystemClsPath = "secretWarScripts.modClient.clientSystem.mainClientSystem.MainClientSystem"

# Engine
Minecraft = "Minecraft"

# 职业常量 & 皮肤材质名
JobsMage = "mage"
JobsHunter = "hunter"

# 可以使用的物品表
canUse = [
    "secret_war:bone_meal_alpaca",
    "secret_war:bone_meal_ender",
    "secret_war:bone_meal_flames",
    "secret_war:bone_meal_illusion",
    "secret_war:bone_meal_spider",
    "secret_war:bone_meal_wolf",
    "secret_war:coin",
    "secret_war:egg_exclusive_precious",
    "secret_war:test"
]

# 每个职业可以捡起和购买的物品
jobsCanUseArms = {
    JobsMage: [
        "secret_war:staff_bursting_blast",
        "secret_war:staff_invigorating",
        "secret_war:staff_slime",
        "secret_war:staff_toxic",
        "secret_war:egg_exclusive_precious_mage",
        "secret_war:attack",
        "secret_war:health"
    ],
    JobsHunter: [
        "secret_war:bow_flame",
        "secret_war:bow_strong",
        "secret_war:bow_hunter",
        "secret_war:bow_antimatter_haz41",
        "secret_war:egg_exclusive_precious_hunter",
        "secret_war:attack",
        "secret_war:health"
    ]
}

# 商店物品价格表
shopItem = {
    "secret_war:staff_bursting_blast": 40,
    "secret_war:staff_invigorating": 30,
    "secret_war:staff_slime": 20,
    "secret_war:staff_toxic": 10,

    "secret_war:bow_flame": 10,
    "secret_war:bow_strong": 20,
    "secret_war:bow_hunter": 30,
    "secret_war:bow_antimatter_haz41": 40,

    "secret_war:egg_exclusive_precious_mage": 15,
    "secret_war:egg_exclusive_precious_hunter": 15,
    "secret_war:attack": 10,
    "secret_war:health": 10,
}

# Attr标识符
ProjectileAttr = "ProjectileAttr"
JobsAttr = "JobsAttr"

# UI
StartGameUIName = "StartGame"
StartGameUIPyClsPath = "secretWarScripts.modClient.ui.startGame.StartGameScreen"
StartGameUIScreenDef = "startGame.main"

JobsSelectUIName = "JobsSelect"
JobsSelectUIPyClsPath = "secretWarScripts.modClient.ui.jobsSelect.JobsSelectScreen"
JobsSelectUIScreenDef = "jobsSelect.main"

CurrencyUIName = "Currency"
CurrencyUIPyClsPath = "secretWarScripts.modClient.ui.currency.CurrencyScreen"
CurrencyUIScreenDef = "currency.main"

ShopMageUIName = "ShopMage"
ShopMageUIPyClsPath = "secretWarScripts.modClient.ui.shopMage.ShopMageScreen"
ShopMageUIScreenDef = "shopMage.main"

ShopHunterUIName = "ShopHunter"
ShopHunterUIPyClsPath = "secretWarScripts.modClient.ui.shopHunter.ShopHunterScreen"
ShopHunterUIScreenDef = "shopHunter.main"

# 自定义事件
JobsSelectEvent = "JobsSelectEvent"
JobsSelectFinished = "JobsSelectFinished"
StartMobsSpawn = "StartMobsSpawn"
PlayerStartButton = "PlayerStartButton"
CreateNPCEvent = "CreateNPCEvent"
PlayerBuyEvent = "PlayerBuyEvent"

ServerCallbackPlayerCurrencyEvent = "ServerCallbackPlayerCurrencyEvent"
ClientGetPlayerCurrencyEvent = "ClientGetPlayerCurrencyEvent"
ClientSetPlayerCurrencyEvent = "ClientSetPlayerCurrencyEvent"

OpenShopEvent = "OpenShopEvent"

#########################

# Server Component
## Engine
EngineTypeComponent = "engineType"
ScriptTypeCompServer = "type"
PosComponent = "pos"
RotComponent = "rot"
BulletComponent = "bulletAttributes"
ModelCompServer = "model"

# Client Component
## Engine
CameraComponent = "camera"
ModelCompClient = "model"
AudioComponent = "customAudio"
ScriptTypeCompClient = "type"
PathComponent = "path"
FrameAniBindComponent = "frameAniEntityBind"
FrameAniTransComponent = "frameAniTrans"
FrameAniCtrlComponent = "frameAniControl"
ParticleTransComponent = "particleTrans"
ParticleControlComponent = "particleControl"
ParticleBindComponent = "particleEntityBind"
## Custom
ClientShootComponent = "ClientShoot"
ClientShootCompClsPath = "secretWarScripts.modClient.clientComponent.shootComponentClient.ShootComponentClient"

# Server Event
## Engine
ServerChatEvent = "ServerChatEvent"
ScriptTickServerEvent = "OnScriptTickServer"
AddServerPlayerEvent = "AddServerPlayerEvent"
ProjectileDoHitEffectEvent = "ProjectileDoHitEffectEvent"
##Custom
PlayShootAnimEvent = "PlayShootAnim"
BulletHitEvent = "BulletHit"
BulletFlyFrameEvent = "BulletFlyFrame"
# Client Event
## Engine
UiInitFinishedEvent = "UiInitFinished"
ScriptTickClientEvent = "OnScriptTickClient"
## Custom
ShootEvent = "Shoot"

# UI
FpsBattleUIName = "fpsBattle"
FpsBattleUIPyClsPath = "secretWarScripts.modClient.ui.fpsBattle.FpsBattleScreen"
FpsBattleUIScreenDef = "fpsBattle.main"

# Client param
SightFieldOfView = -30
DatiangouModel = "datiangou2"
DatiangouRunAnim = "run"
DatiangouFengxiAnim = "fengxi"
DatiangouFengxiAnimFrames = 35
BulletHitSound = "awesome.bullet_hit"
BulletHitEffect = "effects/burst.json"
BulletFlyFrameSfx = "textures/sfxs/snow_3"
ParticleControlFrames = 30

# Server param
BulletPower = 2
BulletGravity = 0.05
