#!/usr/bin/python2.7

from math import *
from gimpfu import *

def plugin_main(timg, tdrawable, inputStr="Hello World", fs=24.0, font_type="Sans Bold"):
	imageList = gimp.image_list()
	image = imageList[0]
	
	#For the text layer
	textLayer = pdb.gimp_text_layer_new(image, inputStr, font_type, fs, 0)
	image.add_layer(textLayer,0)

	tl_x_st = int(floor((image.width - textLayer.width)/2));
	tl_y_st = int(floor((image.height - textLayer.height)/2));

	textLayer.set_offsets(tl_x_st,tl_y_st)

	#Setup the box layer
	boxLayer = pdb.gimp_layer_new(image,image.width,image.height,RGB_IMAGE,"box layer", 100, NORMAL_MODE)
	image.add_layer(boxLayer,0)
	pdb.gimp_layer_add_alpha(boxLayer)
	pdb.gimp_drawable_fill(boxLayer,3)

	# Calculate some dimension
	extra_dim = 20
	box_x_st = tl_x_st - extra_dim/2
	box_y_st = tl_y_st - extra_dim/2

	box_width = textLayer.width + extra_dim
	box_height = textLayer.height + extra_dim

	# Draw the center block
	pdb.gimp_selection_clear(image)
	pdb.gimp_image_set_active_layer(image,boxLayer)
	rect_area = pdb.gimp_image_select_rectangle(image,CHANNEL_OP_ADD,box_x_st,box_y_st, box_width,box_height)
	pdb.gimp_edit_bucket_fill(boxLayer,BG_BUCKET_FILL,NORMAL_MODE,88,15,TRUE,image.width/2, image.height/2)
	
	# Final touch up
	image.lower_layer(boxLayer)
	pdb.gimp_selection_clear(image)

register(
        "insert_center_text",
        "Insert text in the middle of picture",
        "Insert text in the middle of the picture",
        "Yao Hong Kok",
        "Yao Hong Kok",
        "2015",
        "<Image>/Tools/Insert Center Text",
        "RGB*, GRAY*",
        [
                (PF_STRING, "input_str", "Text to input", "Hello World"),
                (PF_FLOAT, "font_size", "Font size", 24.0),
				(PF_STRING, "font_type", "Font type", "Sans Bold"),
        ],
        [],
        plugin_main)

main()
