import java.io.*;
import java.util.Arrays;

Point3D[][] ants;

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
  } finally {
    println("Done Reading");
  }
  size(500, 500);
  fill(255, 50);
  stroke(0, 0);
  strokeWeight(0);
}

void draw() {
  background(50);
  for (int i = 0 ; i < ants.length; i++) {
    Point3D p = ants[i][frameCount%ants[i].length];
    ellipse(p.x*5, p.y*5, p.z, p.z);
  }
//  if (frameCount%4 == 0 && frameCount < ants[0].length) {
//    saveFrame("movie/f######.png");
//  }
}


class Point3D{
  float x, y, z;
  Point3D(float inX, float inY, float inZ){
    this.x = inX;
    this.y = inY;
    this.z = inZ;
  }
}
