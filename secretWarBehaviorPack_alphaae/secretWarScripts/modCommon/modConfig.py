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
canUse = [""]
# 每个职业可以使用的武器表
jobsCanUseArms = {
    JobsMage: ["secret_war:bow_antimatter_haz41"],
    JobsHunter: ["secret_war:bow_flame", "secret_war:bow_strong", "secret_war:bow_hunter"]
}


# Attr标识符
ProjectileAttr = "ProjectileAttr"
JobsAttr = "JobsAttr"

# UI
JobsSelectUIName = "JobsSelect"
JobsSelectUIPyClsPath = "secretWarScripts.modClient.ui.jobsSelect.JobsSelectScreen"
JobsSelectUIScreenDef = "jobsSelect.main"

# 自定义事件
JobsSelectEvent = "JobsSelectEvent"
JobsSelectFinished = "JobsSelectFinished"

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
