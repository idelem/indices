init python:
    class Dice:
        key_map = {
            "name": "名字",
            "n": "面数",
            "sides": "每一面",
        }
        def __init__(self, name=""):
            self.name = name
            self._n = 6
            self.sides = "" # 数字默认转化为整数，其他默认从 images/dice 里取到图片
            self.result = ""
        
        @property
        def side_list(self):
            all_sides = self.sides.split("#")
            if len(all_sides) >= self.n:
                return all_sides[:self.n]
            else:
                return all_sides

        @property
        def n(self):
            return str(self._n)

        @n.setter
        def n(self, value):
            self._n = value
        
        def roll(self):
            self.result = renpy.random.choice(self.side_list)

default dices = []
default dice_map = {}
default dice_icon = Text("没图", xysize=(120,120), background=Solid("#fff"))

screen multi_input(keys, obj):
    # 目前只能编辑字符串字段！
    frame:
        background Solid("#fff")
        has vbox
        for i in range(len(keys)):
            $ k = keys[i]
            $ iv = FieldInputValue(obj, k)
            hbox:
                ysize 32
                $ k_text = obj.key_map[k]
                textbutton k_text xsize 128
                button action Show("single_input", iv=iv, order=i) xfill True:
                    $ ft = getattr(obj, k)
                    text ft
                
        textbutton "填完了" action [Hide("single_input"), Hide("multi_input"), Return()]

screen single_input(iv, order=-1):
    if order >= 0:
        $ yp = order * 36
    else:
        $ yp = 0
    frame:
        background Solid("#fff")
        xpos 128
        ypos yp
        hbox:
            input value iv
            textbutton "√" action Hide("single_input")

screen dicebag():
    vbox:
        textbutton "新建骰子" action Call("make_dice")
        for i in range(len(dices)):
            $ d = dices[i]
            hbox:
                spacing 10
                text d.name
                for ds in d.side_list:
                    if renpy.loadable("images/dice/{}.png".format(ds)):
                        add "images/dice/{}.png".format(ds)
                    else:
                        text ds
                textbutton "我丢" action [Function(d.roll)]
                text "结果：[d.result]"
    pass

screen workbench():
    window:
        background Solid("#ececec")
        hbox:
            textbutton "骰子袋" action Show("dicebag")

label main_menu:
    return

label start:
    window hide
    show screen workbench
    jump workbench

label workbench:
    show screen workbench
    centered ""
    jump workbench

label make_dice:
    python:
        dice = Dice()
    call screen multi_input(["name","n","sides"], dice)
    python:
        if not dice.name: # 简单判空
            renpy.return_statement()
        dices.append(dice)
        dice_map[dice.name] = dice
    return