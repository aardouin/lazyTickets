#!/usr/bin/env python3

import argparse
import csv
import math
import textwrap
import os
import pkg_resources

from PIL import Image, ImageFont, ImageDraw, ImageOps

#Constants 
FONT_RESOURCE = pkg_resources.resource_filename(__name__, "res/Cousine-Regular.ttf")
FONT = ImageFont.truetype(FONT_RESOURCE, 70)
FONT_SMALL= ImageFont.truetype(FONT_RESOURCE, 45)
SOURCE_IMAGE= pkg_resources.resource_filename(__name__, "res/story-task.jpg")
#TASKS_FILENAME = 'Tasks-Table 1.csv'
REMOVED_TAG = 'REMOVED'
ITEMS_PER_PAGE = 3

ITEM_HEIGHT = 1170

LINE_HEIGHT = 105
STORY_ANCHOR_LEFT = 30
STORY_WIDTH = 1600
STORY_BOTTOM_ANCHOR_Y = 1022
CELL_WIDTH = 175
TASK_BOTTOM_ACNCHOR = 2345


DEBUG = True

#Classes 
class Task :
	def __init__(self, raw):
		self.sprint = raw[0]
		self.scenario = raw[3]
		self.tag = raw[4]
		self.what = raw[5]
		self.points = raw[7]

	def __repr__(self):
		return "Task(" + self.tag + ") what = " + self.what

class UserStory :
	def __init__(self, raw):
		self.sprint = raw[0]
		self.scenario = raw[3]
		self.who = raw[4]
		self.what = raw[5]
		self.why = raw[6]
		self.priority = raw[7]
		self.points = raw[8]
		self.tag = ""

	def __repr__(self):
		return "US(" + self.scenario + ") what = " + self.what


#Utility functions 
def writeText(image, text , origin, size, rotate = False, centerX = False, centerY=False, font = FONT):
	txt=Image.new('RGBA', size, color=(255,0,0,50) if DEBUG else (0,0,0,0))
	draw = ImageDraw.Draw(txt)

	if text != "" :
		charSize = draw.textsize(" ",font)
		charPerline = math.floor(size[0] / charSize[0])

		text = "\n".join(textwrap.wrap(text, charPerline))
		
		finalTextSize = draw.multiline_textsize(text,font=font)
		textOrigin  = ( (size[0] - finalTextSize[0] ) / 2 if centerX else 0 ,  (size[1] - finalTextSize[1] ) / 2 if centerY else 0)
		draw.multiline_text( textOrigin, text,font=font, fill=(0,0,0))
	
	if rotate : 
		w=txt.rotate(90,  expand=1)
	else :
		w = txt
		
	image.paste( w, origin ,w)


def writeStory(image, story, indexInPage):
	writeText(image,(story.who), (STORY_ANCHOR_LEFT,72 + indexInPage * ITEM_HEIGHT), (STORY_WIDTH,LINE_HEIGHT), centerY= True)
	writeText(image,(story.what), (STORY_ANCHOR_LEFT,215 + indexInPage * ITEM_HEIGHT), (STORY_WIDTH,365))
	writeText(image,(story.why), (STORY_ANCHOR_LEFT,620 + indexInPage * ITEM_HEIGHT), (STORY_WIDTH,365))
	writeText(image,(story.sprint), (STORY_ANCHOR_LEFT,STORY_BOTTOM_ANCHOR_Y + indexInPage * ITEM_HEIGHT), (CELL_WIDTH,LINE_HEIGHT),centerX = True, centerY = True)
	writeText(image,(story.scenario), (236,STORY_BOTTOM_ANCHOR_Y + indexInPage * ITEM_HEIGHT), (CELL_WIDTH,LINE_HEIGHT),centerX = True, centerY = True , font = FONT_SMALL)
	writeText(image,(story.priority), (448,STORY_BOTTOM_ANCHOR_Y + indexInPage * ITEM_HEIGHT), (CELL_WIDTH,LINE_HEIGHT),centerX = True, centerY = True , font = FONT_SMALL)
	writeText(image,(story.points), (655,STORY_BOTTOM_ANCHOR_Y + indexInPage * ITEM_HEIGHT), (210,LINE_HEIGHT),centerX = True, centerY = True)
	writeText(image,(story.tag), (1163,STORY_BOTTOM_ANCHOR_Y + indexInPage * ITEM_HEIGHT), (320,LINE_HEIGHT),centerX = True, centerY = True)


def writeTask(image, task,indexInPage):
	writeText(image,(task.sprint), (TASK_BOTTOM_ACNCHOR,970 + indexInPage * ITEM_HEIGHT), (CELL_WIDTH,LINE_HEIGHT),rotate = True, centerX= True, centerY = True)
	writeText(image,(task.scenario), (TASK_BOTTOM_ACNCHOR,762 + indexInPage * ITEM_HEIGHT), (CELL_WIDTH,LINE_HEIGHT),rotate = True, centerX= True, centerY = True, font= FONT_SMALL)
	writeText(image,(task.tag), (TASK_BOTTOM_ACNCHOR,348 + indexInPage * ITEM_HEIGHT), (CELL_WIDTH,LINE_HEIGHT),rotate = True, centerX= True, centerY = True)
	writeText(image,(task.points), (TASK_BOTTOM_ACNCHOR,27 + indexInPage * ITEM_HEIGHT), (290,LINE_HEIGHT),rotate = True, centerX= True, centerY = True)
	writeText(image,(task.what), (1700,27 + indexInPage * ITEM_HEIGHT), (1120,600),rotate = True, centerX= True, centerY = True)


def main():
	#Arguments 
	parser = argparse.ArgumentParser(description='Parse csv from packlogs and tranform it to printable tasks / stories')
	parser.add_argument('-sprint','-s' , metavar='S', help='The sprint key representing the sprint' ,required=True)
	parser.add_argument('-file', '-f' ,
	                    help='the path of the backlog csv')
	group = parser.add_mutually_exclusive_group(required=False)
	group.add_argument('--singleTaskStories',"--sts", dest='singleTaskStories', action='store_true',
		help='indicates that you want to print tasks for stories with only one task')
	group.add_argument('--no-singleTaskStories',"--no-sts", dest='singleTaskStories', action='store_false',
		help="(default) indicates that you don't want to print tasks for stories with only one task, instead, the task TAG is added to the story")
	group.set_defaults(singleTaskStories=False)
	args = parser.parse_args()

	csvFileName = args.file
	sprintTag = args.sprint
	singleTaskStories = args.singleTaskStories

	#vars
	taskRows = []
	stories = []
	allTasks = []
	printTasks = []

	#Main function
	csvFile = open(csvFileName)
	backlogReader = csv.reader(csvFile, delimiter=',')

	#tasksCsv = open(csvFolder+ '/' + TASKS_FILENAME)
	#tasksReader = csv.reader(tasksCsv, delimiter=';')

	#for taskRow in tasksReader:
	#	if taskRow[0] == sprintTag: 
	#		allTasks.append(Task(taskRow))
			

	#Compute backlog
	for row in backlogReader:
		if row[0] == REMOVED_TAG : 
			break
		elif row[0] == sprintTag :
			us = UserStory(row)
		#	currentTasks = []
		#	for task in allTasks :
		#		if task.scenario == us.scenario : 
		#			currentTasks.append(task)
			#if singleTaskStories == False and len(currentTasks) == 1 : 
			#	us.tag = currentTasks[0].tag
			#else: 
		#		printTasks.extend( currentTasks )

			stories.append(us)

	nbPages = max( math.ceil(len(stories) / ITEMS_PER_PAGE) , math.ceil(len(printTasks) / ITEMS_PER_PAGE))

	print("UserStories : " + str(len(stories)) + " Tasks : " + str(len(printTasks)))
	print("generating pages ... ")
	for i in range(nbPages):
		print("remaining pages " + str(nbPages - i))
		im=Image.open(SOURCE_IMAGE)

		for j in range(ITEMS_PER_PAGE):
			index = i * ITEMS_PER_PAGE + j
			if index < len(stories):
				writeStory(im,stories[index],j)
			if index < len(printTasks):
				writeTask(im,printTasks[index],j)

		im.save("tickets_"+ str(i) + ".jpg")


#launch main by default
if __name__ == '__main__':
    main()