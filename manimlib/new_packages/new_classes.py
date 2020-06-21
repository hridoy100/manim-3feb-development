from big_ol_pile_of_manim_imports import *


class Grid(VGroup):
    CONFIG = {
        "height": 6.0,
        "width": 6.0,
    }

    def __init__(self, rows, columns, **kwargs):
        digest_config(self, kwargs, locals())
        super().__init__(**kwargs)

        x_step = self.width / self.columns
        y_step = self.height / self.rows

        for x in np.arange(0, self.width + x_step, x_step):
            self.add(Line(
                [x - self.width / 2., -self.height / 2., 0],
                [x - self.width / 2., self.height / 2., 0],
            ))
        for y in np.arange(0, self.height + y_step, y_step):
            self.add(Line(
                [-self.width / 2., y - self.height / 2., 0],
                [self.width / 2., y - self.height / 2., 0]
            ))


class ScreenGrid(VGroup):
    CONFIG = {
        "rows": 8,
        "columns": 14,
        "height": FRAME_Y_RADIUS * 2,
        "width": 14,
        "grid_stroke": 0.5,
        "grid_color": WHITE,
        "axis_color": RED,
        "axis_stroke": 2,
        "labels_scale": 0.25,
        "labels_buff": 0,
        "number_decimals": 2
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rows = self.rows
        columns = self.columns
        grid = Grid(width=self.width, height=self.height, rows=rows, columns=columns)
        grid.set_stroke(self.grid_color, self.grid_stroke)

        vector_ii = ORIGIN + np.array((- self.width / 2, - self.height / 2, 0))
        vector_si = ORIGIN + np.array((- self.width / 2, self.height / 2, 0))
        vector_sd = ORIGIN + np.array((self.width / 2, self.height / 2, 0))

        axes_x = Line(LEFT * self.width / 2, RIGHT * self.width / 2)
        axes_y = Line(DOWN * self.height / 2, UP * self.height / 2)

        axes = VGroup(axes_x, axes_y).set_stroke(self.axis_color, self.axis_stroke)

        divisions_x = self.width / columns
        divisions_y = self.height / rows

        directions_buff_x = [UP, DOWN]
        directions_buff_y = [RIGHT, LEFT]
        dd_buff = [directions_buff_x, directions_buff_y]
        vectors_init_x = [vector_ii, vector_si]
        vectors_init_y = [vector_si, vector_sd]
        vectors_init = [vectors_init_x, vectors_init_y]
        divisions = [divisions_x, divisions_y]
        orientations = [RIGHT, DOWN]
        labels = VGroup()
        set_changes = zip([columns, rows], divisions, orientations, [0, 1], vectors_init, dd_buff)
        for c_and_r, division, orientation, coord, vi_c, d_buff in set_changes:
            for i in range(1, c_and_r):
                for v_i, directions_buff in zip(vi_c, d_buff):
                    ubication = v_i + orientation * division * i
                    coord_point = round(ubication[coord], self.number_decimals)
                    label = Text(f"{coord_point}",font="Arial",stroke_width=0).scale(self.labels_scale)
                    label.next_to(ubication, directions_buff, buff=self.labels_buff)
                    labels.add(label)

        self.add(grid, axes, labels)


class CoordScreen(Scene):
    def construct(self):
        screen_grid = ScreenGrid()
        dot = Dot([1, 1, 0])
        self.add(screen_grid)
        self.play(FadeIn(dot))
        self.wait()


class CheckFormulaByTXT(Scene):
    CONFIG={
    "camera_config":{"background_color": BLACK},
    "svg_type":"text",
    "text": TexMobject(""),
    "file":"",
    "svg_scale":0.9,
    "angle":0,
    "flip_svg":False,
    "fill_opacity": 1,
    "remove": [],
    "stroke_color": WHITE,
    "fill_color": WHITE,
    "stroke_width": 3,
    "numbers_scale":0.5,
    "show_numbers": True,
    "animation": False,
    "direction_numbers": UP,
    "color_numbers": RED,
    "space_between_numbers":0,
    "show_elements":[],
    "color_element":BLUE,
    "set_size":"width",
    "remove_stroke":[],
    "show_stroke":[],
    "warning_color":RED,
    "stroke_":1
    }
    def construct(self):
        self.imagen=self.text
        self.imagen.set_width(FRAME_WIDTH)
        if self.imagen.get_height()>FRAME_HEIGHT:
            self.imagen.set_height(FRAME_HEIGHT)
        self.imagen.scale(self.svg_scale)
        if self.flip_svg==True:
            self.imagen.flip()
        if self.show_numbers==True:
            self.print_formula(self.imagen.copy(),
                self.numbers_scale,
                self.direction_numbers,
                self.remove,
                self.space_between_numbers,
                self.color_numbers)

        self.return_elements(self.imagen.copy(),self.show_elements)
        for st in self.remove_stroke:
            self.imagen[st].set_stroke(None,0)
        for st in self.show_stroke:
            self.imagen[st].set_stroke(None,self.stroke_)
        if self.animation==True:
            self.play(DrawBorderThenFill(self.imagen))
        else:
            c=0
            for j in range(len(self.imagen)):
                permission_print=True
                for w in self.remove:
                    if j==w:
                        permission_print=False
                if permission_print:
                    self.add(self.imagen[j])
            c = c + 1
        self.personalize_image()
        self.wait()

    def personalize_image(self):
        pass

    def print_formula(self,text,inverse_scale,direction,exception,buff,color):
        text.set_color(self.warning_color)
        self.add(text)
        c = 0
        for j in range(len(text)):
            permission_print=True
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add(text[j].set_color(self.stroke_color))
        c = c + 1

        c=0
        for j in range(len(text)):
            permission_print=True
            element = TexMobject("%d" %c,color=color)
            element.scale(inverse_scale)
            element.next_to(text[j],direction,buff=buff)
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add_foreground_mobjects(element)
            c = c + 1 

    def return_elements(self,formula,adds):
        for i in adds:
            self.add_foreground_mobjects(formula[i].set_color(self.color_element),
                TexMobject("%d"%i,color=self.color_element,background_stroke_width=0).scale(self.numbers_scale).next_to(formula[i],self.direction_numbers,buff=self.space_between_numbers))


class ExportCSV(Scene):
    CONFIG={
    "camera_config":{"background_color": BLACK},
    "svg_type":"text",
    "text": TexMobject(""),
    "csv_name":"",
    "csv_number":None,
    "csv_complete":False,
    "csv_name_complete":"no_complete",
    "csv_range":None,
    "csv_desfase":[],
    "cvs_sobrantes":0,
    "file":"",
    "svg_scale":0.9,
    "angle":0,
    "flip_svg":False,
    "fill_opacity": 1,
    "remove": [],
    "stroke_color": WHITE,
    "fill_color": WHITE,
    "stroke_width": 3,
    "numbers_scale":0.5,
    "show_numbers": True,
    "animation": False,
    "direction_numbers": UP,
    "color_numbers": RED,
    "space_between_numbers":0,
    "show_elements":[],
    "color_element":BLUE,
    "set_size":"width",
    "remove_stroke":[],
    "show_stroke":[],
    "warning_color":RED,
    "stroke_":1
    }
    def construct(self):
        self.file_directory=self.__class__.__module__.replace(".", os.path.sep)
        self.directory = os.path.join("csv_files",self.file_directory)
        CSV_DIR=self.directory
        print("\n")
        print("CSV directory at: ",CSV_DIR)

        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)

        self.create_csv()



    def create_csv(self):
        import csv
        self.imagen=self.text
        self.imagen.set_width(FRAME_WIDTH)
        if self.imagen.get_height()>FRAME_HEIGHT:
            self.imagen.set_height(FRAME_HEIGHT)
        self.imagen.scale(self.svg_scale)
        if self.show_numbers==True:
            pre_tex_string,tex_number = self.print_formula(self.imagen.copy(),
                self.numbers_scale,
                self.direction_numbers,
                self.remove,
                self.space_between_numbers,
                self.color_numbers)
        with open(self.directory+'/%s_%s.csv'%(self.__class__.__name__,self.csv_number),'w',newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            tex_string=[]
            if len(self.csv_desfase)==0:
                tex_string=pre_tex_string
            else:
                tex_number_c=tex_number.copy()
                for i in self.remove:
                    tex_number_c.append("x")
                for i in  range(len(tex_number_c)):
                    if i in self.csv_desfase:
                        tex_string.append("DES")
                        tex_string.append(pre_tex_string[i])
                        i+=1
                    else:
                        tex_string.append(pre_tex_string[i])

            data = [
                        tex_number,
                        tex_string
                    ]
            a.writerows(data)

    def print_formula(self,text,inverse_scale,direction,exception,buff,color):
        tex_string=[]
        tex_number=[]
        text.set_color(self.warning_color)
        self.add(text)
        c = 0
        for j in range(len(text)):
            permission_print=True
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add(text[j].set_color(self.stroke_color))
        c = c + 1

        c=0
        for j in range(len(text)):
            permission_print=True
            element = TexMobject("%d" %c,color=color)
            element.scale(inverse_scale)
            element.next_to(text[j],direction,buff=buff)
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add_foreground_mobjects(element)
                tex_string.append(text[j].get_tex_string())
                tex_number.append(j)
            c = c + 1 
        return tex_string,tex_number


class ExportCSVPairs(Scene):
    CONFIG={
    "camera_config":{"background_color": BLACK},
    "svg_type":"text",
    "text": TexMobject(""),
    "csv_name":"",
    "csv_number":None,
    "csv_complete":False,
    "csv_name_complete":"complete",
    "csv_range":None,
    "file":"",
    "directory":"",
    "svg_scale":0.9,
    "angle":0,
    "flip_svg":False,
    "fill_opacity": 1,
    "remove": [],
    "stroke_color": WHITE,
    "fill_color": WHITE,
    "stroke_width": 3,
    "numbers_scale":0.5,
    "show_numbers": True,
    "animation": False,
    "direction_numbers": UP,
    "color_numbers": RED,
    "space_between_numbers":0,
    "show_elements":[],
    "color_element":BLUE,
    "set_size":"width",
    "remove_stroke":[],
    "show_stroke":[],
    "warning_color":RED,
    "stroke_":1
    }
    def construct(self):
        self.file_directory=self.__class__.__module__.replace(".", os.path.sep)
        self.directory = os.path.join("csv_files",self.file_directory)
        CSV_DIR=self.directory
        print("\n")
        print("CSV directory at: ",CSV_DIR)

        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)

        if not self.csv_name==None:
            if not self.csv_complete:
                self.create_csv()
            else:
                self.create_complete_csv()



    def create_csv(self):
        import csv
        self.imagen=self.text
        if self.set_size=="width":
            self.imagen.set_width(FRAME_WIDTH)
        else:
            self.imagen.set_height(FRAME_HEIGHT)
        self.imagen.scale(self.svg_scale)
        if self.show_numbers==True:
            tex_string,tex_number = self.print_formula(self.imagen.copy(),
                self.numbers_scale,
                self.direction_numbers,
                self.remove,
                self.space_between_numbers,
                self.color_numbers)
        with open(self.directory+'/%s_%s.csv'%(self.csv_name,self.csv_number),'w',newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            data = [
                        tex_number,
                        tex_string
                    ]
            a.writerows(data)


    def print_formula(self,text,inverse_scale,direction,exception,buff,color):
        tex_string=[]
        tex_number=[]
        text.set_color(self.warning_color)
        self.add(text)
        c = 0
        for j in range(len(text)):
            permission_print=True
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add(text[j].set_color(self.stroke_color))
        c = c + 1

        c=0
        for j in range(len(text)):
            permission_print=True
            element = TexMobject("%d" %c,color=color)
            element.scale(inverse_scale)
            element.next_to(text[j],direction,buff=buff)
            for w in exception:
                if j==w:
                    permission_print=False
            if permission_print:
                self.add_foreground_mobjects(element)
                tex_string.append(text[j].get_tex_string())
                tex_number.append(j)
            c = c + 1 
        return tex_string,tex_number

    def create_complete_csv(self):
        import csv
        def rango(n):
            return range(n+1)
        def add_quote(row):
            new_row=[]
            for r in row:
                r+=','
                new_row.append(r)
            return new_row
        def es_par(n):
            if n%2==0:
                return True
            else:
                return False


        rows=[]
        list_0=list(range(self.csv_range))
        list_1=list_0.copy()

        list_1.append(self.csv_range)
        list_1.pop(0)

        for f_i,f_f in zip(list_0,list_1):
            for string in range(f_i,f_f+1):
                pre_rows=[]
                with open(self.directory+'/%s_%s.csv'%(self.csv_name,string), 'r') as f:
                    reader = csv.reader(f,delimiter=',')
                    for row in reader:
                        pre_rows.append(row)
                    if string==f_i:
                        rows.append(['Step: %s'%(f_i+1)])
                        rows.append(['\t']+['N']+add_quote(pre_rows[0])+['),'])
                        rows.append(['\t']+['[%s]'%f_i]+pre_rows[1])
                    else:
                        rows.append(['\t']+['[%s]'%f_f]+pre_rows[1])
                        rows.append(['\t']+['N']+add_quote(pre_rows[0])+[')'])
                        rows.append("\n")
                        rows.append(['pre_fade:']+['('])
                        rows.append(['pre_write:']+['('])
                        rows.append(['pre_copy:']+['('])
                        rows.append("\n")
                        rows.append(['pre_form:']+['('])
                        rows.append(['pos_form:']+['('])
                        rows.append("\n")
                        rows.append(['pos_copy:']+['('])
                        rows.append(['pos_fade:']+['('])
                        rows.append(['pos_write:']+['('])
                        rows.append("\n")
                        rows.append(['run_fade:']+['('])
                        rows.append(['run_write:']+['('])
                        rows.append("\n")
                        rows.append(['---------']*50)
                        rows.append("\n")




        with open(self.directory+'/%s.csv'%self.csv_name,'w',newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            data = [
                      *rows
                    ]
            a.writerows(data)

