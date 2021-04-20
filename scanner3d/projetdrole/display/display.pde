int t;
float s = 8;
String[] lines;
String[][] ts;
int eltiempo=0;
void setup() {
  size(500,500);
  lines = loadStrings("todisplay.txt");
  strokeWeight(1);
  
  t=0;
  
}

void draw() {
  eltiempo = frameCount;
  background(255);
  translate(width/2,height/2);
    for (int i=0;i<lines.length;i++) {
      String[] splitted = lines[i].split(" ");
      if (splitted[0].charAt(0) == 't') {
        t = int(splitted[1]);
      }
      if (eltiempo == t){
      if (splitted[0].charAt(0) == 'l') {
        line(float(splitted[1])*s, -float(splitted[2])*s, float(splitted[3])*s, -float(splitted[4])*s);
      }
      if (splitted[0].charAt(0) == 'p') {
        point(float(splitted[1])*s, -float(splitted[2])*s);
      }
      if (splitted[0].charAt(0) == 'c') {
        stroke(float(splitted[1]), float(splitted[2]), float(splitted[3]),255);
      }
      if (splitted[0].charAt(0) == 'k') {
        stroke(float(splitted[1]), float(splitted[2]), float(splitted[3]),60);
      }
      
     }
    }
    if (eltiempo<150) {
      saveFrame("onsauvegarde/"+nf(eltiempo,5)+".png");
    }
    else {
      exit();
    }
    
}

void mousePressed() {
  if (mouseButton==RIGHT) {eltiempo+=1;println(eltiempo);}
  else if (mouseButton==LEFT) {eltiempo--;println(eltiempo);}
  else {
    println((mouseX-250)/s,(500-mouseY-250)/s);
  }
}
