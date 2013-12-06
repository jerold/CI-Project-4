import java.io.*;
import java.util.Arrays;

Point3D[] particles;
Point3D[] patterns;

int xMin, xMax, yMin, yMax;

void setup() {
  int windowSize = 500;
  size(windowSize, windowSize);
  
  xMin = 99999;
  xMax = 0;
  yMin = 99999;
  yMax = 0;
 
  try {
    String lines[] = loadStrings("psoMembers.csv");
    println("there are " + lines.length + " lines");
    float[] numbers = float(split(lines[0], ','));
    int partCount = int(numbers[0]);
    int partStart = 1;
    int partLength = 2;
    particles = new Point3D[partCount];
    for (int i = 0 ; i < partCount; i++) {
      particles[i] = new Point3D(numbers[i*partLength+partStart], numbers[i*partLength+partStart+1], 0);
      if (numbers[i*partLength+partStart] > xMax)
        xMax = int(numbers[i*partLength+partStart] + 0.5);
      if (numbers[i*partLength+partStart] < xMin)
        xMin = int(numbers[i*partLength+partStart] - 0.5);
      if (numbers[i*partLength+partStart+1] > yMax)
        yMax = int(numbers[i*partLength+partStart+1] + 0.5);
      if (numbers[i*partLength+partStart+1] < yMin)
        yMin = int(numbers[i*partLength+partStart+1] - 0.5);
    }
    int patCount = int(numbers[partCount*(partLength)+partStart]);
    int patStart = partCount*(partLength)+partStart + 1;
    int patLength = 3;
    patterns = new Point3D[patCount];
    for (int i = 0 ; i < patCount; i++) {
      patterns[i] = new Point3D(numbers[i*patLength+patStart], numbers[i*patLength+patStart+1], numbers[i*patLength+patStart+2]);
      if (numbers[i*patLength+patStart] > xMax)
        xMax = int(numbers[i*patLength+patStart] + 0.5);
      if (numbers[i*patLength+patStart] < xMin)
        xMin = int(numbers[i*patLength+patStart] - 0.5);
      if (numbers[i*patLength+patStart+1] > yMax)
        yMax = int(numbers[i*patLength+patStart+1] + 0.5);
      if (numbers[i*patLength+patStart+1] < yMin)
        yMin = int(numbers[i*patLength+patStart+1] - 0.5);
    }
    
    float xScale = float(windowSize)/(xMax - xMin);
    float yScale = float(windowSize)/(yMax - yMin);
    println("Max: " + xMax + "," + yMax + ", Scale:" + xScale);
    println("Min: " + xMin + "," + yMin + ", Scale:" + yScale);
    
    // Normalize
    for (int i = 0 ; i < partCount; i++) {
      particles[i].x = (particles[i].x - xMin)*xScale;
      particles[i].y = (particles[i].y - yMin)*yScale;
    }
    for (int i = 0 ; i < patCount; i++) {
      patterns[i].x = (patterns[i].x - xMin)*xScale;
      patterns[i].y = (patterns[i].y - yMin)*yScale;
    }
  } 
  finally {
    println("Done Reading");
  }
}

void draw() {
  background(40);
  
  fill(0, 0);
  stroke(120, 180, 150, 150);
  strokeWeight(2);
  for (int i = 0 ; i < particles.length; i++) {
    Point3D p = particles[i];
    ellipse(p.x, p.y, 10, 10);
  }
  stroke(120, 150, 180, 150);
  for (int i = 0 ; i < patterns.length; i++) {
    Point3D p = patterns[i];
    Point3D p2 = particles[int(p.z)];
    ellipse(p.x, p.y, 4, 4);
    line(p.x, p.y, p2.x, p2.y);
  }
  
}

class Point3D {
  float x, y, z;
  Point3D(float inX, float inY, float inZ) {
    this.x = inX;
    this.y = inY;
    this.z = inZ;
  }
}

