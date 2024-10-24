# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi
CustomUIScreenProxy = clientApi.GetUIScreenProxyCls()

CompFactory = clientApi.GetEngineCompFactory()
ROOT_PANEL_PATH = "variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/"
CLASSICAL_HEART_REND_PATH = "centered_gui_elements_at_bottom_middle/heart_rend"
POCKET_HEART_REND_PATH = "not_centered_gui_elements/heart_rend"
import zaibian.modCommon.modConfig as modConfig


class PyClientScreen(CustomUIScreenProxy):
    def __init__(self, screenName, screenNode):
        CustomUIScreenProxy.__init__(self, screenName, screenNode)
        self.data=['','','','',"","",""]

        self.data1={"狂刃魔君":8,"远古遗魂":7," 利维坦 ":6,"利维坦":5," 焰魔 ":4,"焰魔":3,"先驱者":2,"末影守卫":1,"下界合金巨兽":0}

        self.size=[9,9,9,9,9,16,16,28,10]

        self.misss={" 焰魔 ":"ignis_theme","焰魔":"ignis_theme","先驱者":"harbinger_theme",
        "末影守卫":"enderguardian_theme","下界合金巨兽":"monstrosity_theme",
        " 利维坦 ":"leviathan_theme","利维坦":"leviathan_theme","远古遗魂":"remnant_theme",
        "狂刃魔君":"remnant_theme",
        
        }

        self.musicId=None
        self.musicName=""

        
        self.tick=0


        self.strat=False

        self.sandUI=[False for i in range(10)]

    

    def OnCreate(self):
        self.strat=True

        print("PauseScreenProxy Create")
        # 在pause.pause_screen被pushed的时候创建一个button以及一个toggle
        self1 = self.GetScreenNode()

        p="variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/centered_gui_elements_at_bottom_middle"
        p1="variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/not_centered_gui_elements"
        parentControl = self1.GetBaseUIControl(p)
        if parentControl:
            childNode = self1.CreateChildControl("pinga.sand", "sand", parentControl, True)

        parentControl = self1.GetBaseUIControl(p1)
        if parentControl:
            childNode = self1.CreateChildControl("pinga.sand", "sand", parentControl, True)
            

    def OnDestroy(self):
        comp = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLevelId())
        comp.StopCustomMusic(self.musicId, 0)
        self.musicId=None
        self.strat=False

        print("PauseScreenProxy Destroy")


                
    def set_cj(self):
        path1_="variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/goodBtn"
        self1 = self.GetScreenNode()

        baseUIControl = self1.GetBaseUIControl(path1_)
        textVisible = baseUIControl.SetVisible(False)

    def OnTick(self):
        self.tick+=1

        if not  self.strat or not clientApi:
            return
        
        if self.tick%1==0:
            self1 = self.GetScreenNode()
            if self1:
                comp = clientApi.GetEngineCompFactory().CreateModAttr(clientApi.GetLocalPlayerId())
                uisand=comp.GetAttr('uisand')
                init_ui=180
                p_1="variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/centered_gui_elements_at_bottom_middle/"
                p_2="variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/not_centered_gui_elements"

                for p in [p_1,p_2]:
                    comp = clientApi.GetEngineCompFactory().CreatePlayerView(clientApi.GetLevelId())
                    profile = comp.GetUIProfile()
                    if not  ((profile==1 and p==p_2 )or  (profile==0 and p==p_1)):
                        continue
                    if uisand<init_ui:
                        w=int(uisand/float(init_ui/10))
                        if uisand<1:
                            w=-1
                        i=-1
                        for i in range(w+1):
                            pa=p+"/sand/"+str(i)
                            imageUIControl = self1.GetBaseUIControl(pa).asImage()
                            imageUIControl.SetSpriteUV((0, 0))
                            self.sandUI[i]=True
                            if i==9:
                                baseUIControl = self1.GetBaseUIControl(p+"/sand")
                                comp1 = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
                                comp1.AddTimer(1,baseUIControl.SetVisible,False)
                        if 1+i<10 and  self.sandUI[1+i]:
                            self.sandUI[1+i]=False
                            pa=p+"/sand/"+str(1+i)
                            text1Control = self1.GetBaseUIControl(pa)
                            if text1Control:
                                text1Control.resetAnimation()
                            self1.UpdateScreen(True)
                        baseUIControl = self1.GetBaseUIControl(p+"/sand")
                        if not  baseUIControl.GetVisible():
                            kl=0
                            comp = clientApi.GetEngineCompFactory().CreatePlayer(clientApi.GetLocalPlayerId())
                            if comp.isInWater():
                                kl+=1
                            baseUIControl1 = self1.GetBaseUIControl(p+"/sand")
                            if profile==0:
                                pos = (100, -kl*10)
                            else:
                                baseUIControl = self1.GetBaseUIControl(p)
                                text2Size = baseUIControl.GetSize()
                                pos = (text2Size[0]-80, 10+kl*10)
                            baseUIControl1.SetPosition(pos)
                            baseUIControl.SetVisible(True)
                            




        if self.tick%8!=0:
            return
        
        self1 = self.GetScreenNode()
        
        if not self1:
            return
        client=clientApi.GetSystem(modConfig.ModName,modConfig.ClientSystemName)
        client.boss_ui=self


        

        

        

                
        
        path="variables_button_mappings_and_controls/safezone_screen_matrix/inner_matrix/safezone_screen_panel/root_screen_panel/root_panel/boss_health_panel/boss_hud_panel/boss_health_grid"
        list1=self1.GetChildrenName(path)
        

        key=0
        if not list1:
            return
        for i in list1:
            path1=path+"/"+i
            name=path+"/"+i+'/boss_name/boss_name'
            tp=path+"/"+i+'/progress_bar_for_collections/empty_progress_bar'
            tp1=path+"/"+i+'/progress_bar_for_collections/filled_progress_bar_for_collections1'
            tp2=path+"/"+i+'/progress_bar_for_collections/filled_progress_bar_for_collections'

            progress_bar_for_collections=path+"/"+i+'/progress_bar_for_collections'
            
            val=int(i[-1])-1
            baseUIControl = self1.GetBaseUIControl(path1)
            textVisible = baseUIControl.GetVisible()
            if textVisible:
                
                labelUIControl = self1.GetBaseUIControl(name).asLabel()
                n=labelUIControl.GetText()
                if n in self.data1.keys():
                    if (not self.musicId or ( self.musicId not in self.misss[n]) )and self.musicName!=self.misss[n] and key==0:
                        comp = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLevelId())
                        comp.PlayGlobalCustomMusic(self.misss[n], 1, True)
                        self.musicId=self.misss[n]
                        self.musicName=self.misss[n]
                    key=1
                    if n!=self.data[val]:
                        
                        def f(n,i):
                            name=path+"/"+i+'/boss_name/boss_name'
                            progress_bar_for_collections=path+"/"+i+'/progress_bar_for_collections'

                            tp=path+"/"+i+'/progress_bar_for_collections/empty_progress_bar'
                            tp1=path+"/"+i+'/progress_bar_for_collections/filled_progress_bar_for_collections1'
                            tp2=path+"/"+i+'/progress_bar_for_collections/filled_progress_bar_for_collections'

                            val=int(i[-1])-1
                            size=0
                            for i in range(self.data1[n]):
                                size+=self.size[i]

                            self1.GetBaseUIControl(tp).SetLayer(2,False)
                            self1.GetBaseUIControl(tp1).SetLayer(1,False)

                            if self.size[self.data1[n]]==27:
                                absoluteValue=27
                                
                            else:
                                absoluteValue=self.size[self.data1[n]]-1
                            self1.GetBaseUIControl(name).SetLayer(100,False)
                            imageUIControl = self1.GetBaseUIControl(tp).asImage()
                            imageUIControl.SetSpriteUV((0, size))
                            baseUIControl = self1.GetBaseUIControl(tp)
                            ret = baseUIControl.SetFullSize(axis="y", paramDict={"absoluteValue":absoluteValue, "followType":"children", "relativeValue":1})
                            ret = baseUIControl.SetFullPosition(axis="y", paramDict={"followType":"parent", "relativeValue":0.5})
                            baseUIControl = self1.GetBaseUIControl(tp1)
                            ret = baseUIControl.SetFullSize(axis="y", paramDict={"absoluteValue":absoluteValue, "followType":"children", "relativeValue":1})
                            ret = baseUIControl.SetFullPosition(axis="y", paramDict={"followType":"parent", "relativeValue":0.5})
                            self.data[val]=n
                            buttonUIControl = self1.GetBaseUIControl(tp).asImage()
                            buttonUIControl.SetSprite("textures/ui/boss_bar_frames")
                            imageUIControl = self1.GetBaseUIControl(tp).asImage()
                            imageUIControl.SetSpriteUVSize((189, self.size[self.data1[n]]))
                            buttonUIControl.SetImageAdaptionType("oldNineSlice")

                            buttonUIControl = self1.GetBaseUIControl(tp1).asImage()
                            buttonUIControl.SetSprite("textures/ui/boss_bar_strip")

                            buttonUIControl.SetSpriteUV((0, size))
                            imageUIControl = self1.GetBaseUIControl(tp1).asImage()
                            imageUIControl.SetSpriteUVSize((189, self.size[self.data1[n]]))
                            buttonUIControl.SetImageAdaptionType("oldNineSlice")

                            imageUIControl = self1.GetBaseUIControl(tp1).asImage()
                            imageUIControl.SetSpriteColor((1, 1, 1))




                            imageUIControl = self1.GetBaseUIControl(tp2).asImage()
                            imageUIControl.SetVisible(False)
                            imageUIControl = self1.GetBaseUIControl(tp1).asImage()
                            imageUIControl.SetVisible(True)
                            #######
                            # parentControl = self1.GetBaseUIControl(progress_bar_for_collections)
                            # if parentControl:
                            #     list1=self1.GetChildrenName(progress_bar_for_collections)
                            #     if '333' not in list1:
                            #         childNode = self1.CreateChildControl("pinga.filled_progress_bar", "333", parentControl, True)
                            # buttonUIControl = self1.GetBaseUIControl(progress_bar_for_collections+"/333").asImage()
                            # buttonUIControl.SetVisible(True)
                            # self1.GetBaseUIControl(progress_bar_for_collections+"/333").SetLayer(1,False)

               
                                                    
                        comp1 = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
                        comp1.AddTimer(0.0,f,n,i)

                else:
                    key_=client.set_data.get("6",False) 
                    if self.data[val] in  self.data1.keys():
                        self1.GetBaseUIControl(tp).SetLayer(1,False)
                        self1.GetBaseUIControl(tp1).SetLayer(2,False)

                        imageUIControl = self1.GetBaseUIControl(tp).asImage()
                        imageUIControl.SetSpriteUV((0, 0))
                        baseUIControl = self1.GetBaseUIControl(tp)
                        ret = baseUIControl.SetFullSize(axis="y", paramDict={"absoluteValue":5, "followType":"children", "relativeValue":1})
                        ret = baseUIControl.SetFullPosition(axis="y", paramDict={"followType":"parent", "relativeValue":0.0})
                        baseUIControl = self1.GetBaseUIControl(tp1)
                        ret = baseUIControl.SetFullSize(axis="y", paramDict={"absoluteValue":5, "followType":"children", "relativeValue":1})
                        ret = baseUIControl.SetFullPosition(axis="y", paramDict={"followType":"parent", "relativeValue":0.0})
                        self.data[val]=n
                        buttonUIControl = self1.GetBaseUIControl(tp).asImage()
                        buttonUIControl.SetSprite("textures/ui/empty_progress_bar")
                        buttonUIControl.SetSpriteUVSize((0, 0))
                        buttonUIControl.SetImageAdaptionType("originNineSlice")

                        buttonUIControl = self1.GetBaseUIControl(tp1).asImage()
                        buttonUIControl.SetSpriteUV((0, 0))
                        buttonUIControl.SetSprite("textures/ui/filled_progress_bar")
                        buttonUIControl.SetSpriteUVSize((0, 0))
                        buttonUIControl.SetImageAdaptionType("originNineSlice")
                        imageUIControl = self1.GetBaseUIControl(tp1).asImage()
                        imageUIControl.SetSpriteColor((1, 1, 1))

                    imageUIControl = self1.GetBaseUIControl(tp2).asImage()
                    if imageUIControl.GetVisible != (not key_):
                        imageUIControl.SetVisible(not key_)
                        imageUIControl = self1.GetBaseUIControl(tp1).asImage()
                        imageUIControl.SetVisible(key_)

   
        def f1():
            key=0
            for i in list1:
                path1=path+"/"+i
                name=path+"/"+i+'/boss_name/boss_name'
                baseUIControl = self1.GetBaseUIControl(path1)
                textVisible = baseUIControl.GetVisible()
                if textVisible:
                    labelUIControl = self1.GetBaseUIControl(name).asLabel()
                    n=labelUIControl.GetText()
                    if n in self.data1.keys():
                        key=1
                        break
            if key==0:
                if self.musicId:
                    comp = clientApi.GetEngineCompFactory().CreateCustomAudio(clientApi.GetLevelId())
                    comp.StopCustomMusic(self.musicId, 0)
                    self.musicId=None
                    self.musicName=""
        if key==0:
            comp = clientApi.GetEngineCompFactory().CreateGame(clientApi.GetLevelId())
            comp.AddTimer(2,f1)

