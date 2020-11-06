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

# 职业常量
JobsMage = "mage"
JobsHunter = "hunter"

# 抛射物标识符
ProjectileAttr = "ProjectileAttr"

# UI
JobsSelectUIName = "JobsSelect"
JobsSelectUIPyClsPath = "secretWarScripts.modClient.ui.jobsSelect.JobsSelectScreen"
JobsSelectUIScreenDef = "jobsSelect.main"

# 自定义事件
JobsSelectEvent = "JobsSelectEvent"

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
