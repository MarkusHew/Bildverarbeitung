#####################################################################
# --- DO NOT EDIT THE CODE BELOW  --- #
# input: 
#    orig = input image
# output:
#    proc = processed image
orig = orig.astype(float); thresh = 100; #Bildmatrix muss erst in Gleitkommazahlen umgewandelt werden!!

#####################################################################
# --- START EDITING HERE  --- #
# proc = orig * 0.3; #Bildhelligkeit
# proc = 255-orig;  #Differenz zu weiss -> invertiert              
# proc = orig; proc[proc < thresh]=thresh; #setzt alle Pixelwerte<100 auf 100 -> alle dunklen Pixel entfernen, nennt sich clipping
# proc = 255/(100-50)*(orig-50); proc = np.maximum(np.minimum(proc,255),0); #werte liegen jetzt zwischen 0 und 255(hinterer Teil), lineare Grauwertspreizung(vorderer Teil)
# proc = np.power(orig/255,2)*255;    #weiss bleibt weiss, dynamischer Bereich wird aufgespreizt
#proc = (orig > thresh)*255;   #Linearisierung, gibt nur noch 2 Helligkeitswerte
# proc = np.floor(orig / 50) * 50; #floor rundet nach unten ab, Grauwerte reduzieren

#Aufgabe Skriptaufgabe 02-9
proc = np.floor(orig / 256/3) * floor(256/3); #floor rundet nach unten ab, Grauwerte reduzieren

# end of image modification
#####################################################################
