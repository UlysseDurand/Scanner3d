#!/bin/sh
rm entree/*
cp generate/res/* entree/
convert -delay 10 -loop 0 entree/*.png entree.gif 