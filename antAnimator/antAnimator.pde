import java.io.*;
import java.util.Arrays;

Point3D[][] ants;
Button[] buttons;
int ffRate;
int frameNumber;
int eScale;
int realSize;
boolean playing;
boolean mouseDown;

void setup() {
  realSize = 100;
  eScale = 4;
  size(realSize*(eScale+1), realSize*(eScale+1));

  String filename=dataPath("antMotion.csv");
  try {
    String lines[] = loadStrings("antMotion.csv");
    println("there are " + lines.length + " lines");
    for (int i = 0 ; i < lines.length; i++) {
      float[] numbers = float(split(lines[i], ','));
      if (i == 0) {
        ants = new Point3D[lines.length][numbers.length/3];
      }
      println("Ant " + i + " has " + numbers.length/3 + " points");
      for (int j = 0 ; j < numbers.length/3; j++) {
        ants[i][j] = new Point3D(numbers[j*3], numbers[j*3+1], numbers[j*3+2]);
        //println(numbers[j*2] + " : " + numbers[j*2+1]);
      }
    }
  } finally {
    println("Done Reading");
  }
  
  buttons = new Button[6];
  buttons[0] = new Button("1x", 10, 10);
  buttons[1] = new Button("10x", 110, 10);
  buttons[1].active = true;
  buttons[2] = new Button("100x", 210, 10);
  
  buttons[3] = new Button("Start", 10, height-30);
  buttons[4] = new Button("Pause", 110, height-30);
  buttons[5] = new Button("End", 210, height-30);
  
  ffRate = 10;
  frameNumber = 0;
  playing = true;
  mouseDown = false;
  
  fill(255, 50);
  stroke(0, 0);
  strokeWeight(0);
}

void draw() {
  background(255);
  background(40);
  
  if (playing) {
    frameNumber+=ffRate;
  }

  //int drawFrame = min(frameNumber, ants[0].length-1);
  int drawFrame = (frameNumber)%ants[0].length;
  //int drawFrame = ants[0].length-1;
  // int drawFrame = 0;
  
  for (int i = 0 ; i < buttons.length; i++) {
    buttons[i].drawButton();
  } 
  
  if (mousePressed && !mouseDown) {
    mouseDown = true;
    for (int i = 0 ; i < buttons.length; i++) {
      if (buttons[i].hovering() && i < 3) {
        buttons[i].active = true;
      } else {
        buttons[i].active = false;
      }
      
      if (i==0 && buttons[i].hovering())
        ffRate = 1;
      if (i==1 && buttons[i].hovering())
        ffRate = 10;
      if (i==2 && buttons[i].hovering())
        ffRate = 100;
      if (i==3 && buttons[i].hovering()) {
        frameNumber = 0;
        playing = false;
      }
      if (i==4 && buttons[i].hovering()) {
        if(buttons[i].t.equals("Play")) {
          buttons[i].t = "Pause";
          playing = true;
        } else {
          buttons[i].t = "Play";
          playing = false;
        }
      }
      if (i==5 && buttons[i].hovering()) {
        frameNumber = ants[0].length-1;
        playing = false;
      }
    }
  } else if (!mousePressed && mouseDown) {
    mouseDown = false;
  }
  
  for (int i = 0 ; i < ants.length; i++) {
    Point3D p = ants[i][drawFrame];
    // fill(120, 150, 180, 20);
    fill(0, 0);
    if (p.z == 200) {
      stroke(120, 180, 150, 150);
    } else {
      stroke(120, 150, 180, 150-(p.z/1.5));
    }
    // stroke(0, 0, 0, 150);
    strokeWeight(3);
    // ellipse(p.x*4+50, p.y*4+50, p.z*0.3, p.z*0.3);
    ellipse(p.x*eScale+50, p.y*eScale+50, p.z/3+2, p.z/3+2);
    strokeWeight(1);
    int inc = 0;
    for (int j = drawFrame-1; j >=max(0, drawFrame-20); j--) {
      stroke(180, 120, 150, 200-inc*10);
      if (ants[i][j+1].distance(ants[i][j]) < 30) {
        line(ants[i][j+1].x*eScale+50, ants[i][j+1].y*eScale+50, ants[i][j].x*eScale+50, ants[i][j].y*eScale+50);
      }
      inc++;
    }
  }

  // Isolate final frame
  //  fill(50, 150, 50, 50);
  //  for (int i = 0 ; i < ants.length; i++) {
  //    Point3D p = ants[i][ants[i].length-1];
  //    ellipse(p.x*4+50, p.y*4+50, 5, 5);
  //  }
  //  fill(150, 50, 50, 50);
  //  for (int i = 0 ; i < ants.length; i++) {
  //    Point3D p = ants[i][0];
  //    ellipse(p.x*4+50, p.y*4+50, 5, 5);
  //  }
  fill(255, 150);
  textAlign(RIGHT, BOTTOM);
  text(drawFrame, width-10, height-30);
  text(ants[0].length-1, width-10, height-10);
  textAlign(LEFT, BOTTOM);

//  if (playing)
//    text("Play", width-60, 20);
//  else
//    text("Pause", width-60, 20);
//  if (mouseDown)
//    text("Down", width-60, 40);
  //  if (frameCount*ffRate < ants[0].length) {
  //    saveFrame("movie/f######.png");
  //  }
}

class Point3D {
  float x, y, z;
  Point3D(float inX, float inY, float inZ) {
    this.x = inX;
    this.y = inY;
    this.z = inZ;
  }
  
  float distance(Point3D p2) {
    return sqrt(pow(this.x - p2.x, 2) + pow(this.y - p2.y, 2));
  }
}

class Button {
  int x, y, hw;
  String t;
  boolean active;
  Button(String text, int x, int y) {
    this.t = text;
    this.x = x;
    this.y = y;
    this.hw = 20;
    this.active = false;
  }
  
  void drawButton() {
    stroke(255, 100);
    strokeWeight(2);
    fill(255, 40);
    if (this.active) {
      fill(255, 200);
    } else if (hovering()) {
      fill(255, 160);
    }
    rect(this.x, this.y, this.hw, this.hw);
    textAlign(LEFT, CENTER);
    text(t, x+this.hw*1.5, y+this.hw*.5);
    textAlign(LEFT, BOTTOM);
  }
  
  boolean hovering() {
    if (mouseX > this.x && mouseX < this.x + hw*4) {
      if (mouseY > this.y && mouseY < this.y + hw) {
        return true;
      }
    }
    return false;
  }
}
