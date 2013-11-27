import java.io.*;
import java.util.Arrays;

Point3D[][] ants;
int ffRate;
int eScale;
int realSize;

void setup() {
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
  } 
  finally {
    println("Done Reading");
  }
  
  realSize = 100;
  eScale = 5;
  
  size(realSize*eScale, realSize*eScale);
  fill(255, 50);
  stroke(0, 0);
  strokeWeight(0);
  ffRate = 10;
}

void draw() {
  //int drawFrame = (frameCount*ffRate)%ants[0].length;
  //int drawFrame = ants[0].length-1;
  int drawFrame = 0;
  
  background(255);
  // background(40);
  for (int i = 0 ; i < ants.length; i++) {
    Point3D p = ants[i][drawFrame];
    if (i >= 155) {
      fill(180, 180, 180, 20);
      stroke(0, 0);
      strokeWeight(0);
      ellipse(p.x*4+50, p.y*4+50, p.z*3, p.z*3);
    } else if (i >= 150) {
      fill(0, 0);
      // stroke(120, 180, 150, 150);
      strokeWeight(3);
      ellipse(p.x*4+50, p.y*4+50, 20*eScale, 20*eScale);
    } else {
      // fill(120, 150, 180, 20);
      fill(0, 0);
      // stroke(120, 150, 180, 150);
      stroke(0, 0, 0, 150);
      strokeWeight(3);
      // ellipse(p.x*4+50, p.y*4+50, p.z*0.3, p.z*0.3);
      ellipse(p.x*4+50, p.y*4+50, 6*eScale, 6*eScale);
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
  text(drawFrame, 20, 460);
  text(ants[0].length, 20, 480);
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
}

