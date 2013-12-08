import java.io.*;
import java.util.Arrays;

Point3D[] particleBests;
Point3D[][] particlePositions;
Point3D[] patternPositions;
int[][] patternMembership;

int xMin, xMax, yMin, yMax, frames;

void setup() {
  int windowSize = 500;
  int edgeWidth = 10;
  size(windowSize + 2*edgeWidth, windowSize + 2*edgeWidth);
  
  xMin = 99999;
  xMax = 0;
  yMin = 99999;
  yMax = 0;
 
  try {
    String lines[] = loadStrings("psoMembers.csv");
    println("there are " + lines.length + " lines");
    float[] numbers = float(split(lines[0], ','));
    frames = split(lines[10], ',').length/2; // x and y values so divide this by 2
    println(frames);
    
    // Initialize all of the particles and patterns
    int partCount = int(numbers[0]);
    int partStart = 1;
    int partLength = 2;
    particleBests = new Point3D[partCount];
    particlePositions = new Point3D[partCount][frames];
    for (int i = 0 ; i < partCount; i++) {
      particleBests[i] = new Point3D(numbers[i*partLength+partStart], numbers[i*partLength+partStart+1], 0);
      
      float[] positionNumbers = float(split(lines[i+1], ','));
      for (int j = 0 ; j < frames; j++) {
        Point3D p = new Point3D(positionNumbers[j*2], positionNumbers[j*2+1], 0);
        particlePositions[i][j] = p;

        if (p.x > xMax)
          xMax = int(p.x + 0.5);
        if (p.x < xMin)
          xMin = int(p.x - 0.5);
        if (p.y > yMax)
          yMax = int(p.y + 0.5);
        if (p.y < yMin)
          yMin = int(p.y - 0.5);
      }
    }
    
    int patCount = int(numbers[partCount*(partLength)+partStart]);
    int patStart = partCount*(partLength)+partStart + 1;
    int patLength = 3;
    patternPositions = new Point3D[patCount];
    patternMembership = new int[patCount][frames];
    for (int i = 0 ; i < patCount; i++) {
      patternPositions[i] = new Point3D(numbers[i*patLength+patStart], numbers[i*patLength+patStart+1], numbers[i*patLength+patStart+2]);
      if (numbers[i*patLength+patStart] > xMax)
        xMax = int(numbers[i*patLength+patStart] + 0.5);
      if (numbers[i*patLength+patStart] < xMin)
        xMin = int(numbers[i*patLength+patStart] - 0.5);
      if (numbers[i*patLength+patStart+1] > yMax)
        yMax = int(numbers[i*patLength+patStart+1] + 0.5);
      if (numbers[i*patLength+patStart+1] < yMin)
        yMin = int(numbers[i*patLength+patStart+1] - 0.5);

      float[] membershipNumbers = float(split(lines[partCount+i+1], ','));
      for (int j = 0 ; j < frames; j++) {
        patternMembership[i][j] = int(membershipNumbers[j]);
      }  
    }
    
    float xScale = float(windowSize)/(xMax - xMin);
    float yScale = float(windowSize)/(yMax - yMin);
    println("Max: " + xMax + "," + yMax + ", Scale:" + xScale);
    println("Min: " + xMin + "," + yMin + ", Scale:" + yScale);
    
    // Normalize
    for (int i = 0 ; i < partCount; i++) {
      particleBests[i].x = (particleBests[i].x - xMin)*xScale + edgeWidth;
      particleBests[i].y = (particleBests[i].y - yMin)*yScale + edgeWidth;
      for (int j = 0 ; j < frames; j++) {
        particlePositions[i][j].x = (particlePositions[i][j].x - xMin)*xScale + edgeWidth;
        particlePositions[i][j].y = (particlePositions[i][j].y - yMin)*yScale + edgeWidth;
      }
    }
    for (int i = 0 ; i < patCount; i++) {
      patternPositions[i].x = (patternPositions[i].x - xMin)*xScale + edgeWidth;
      patternPositions[i].y = (patternPositions[i].y - yMin)*yScale + edgeWidth;
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
  for (int i = 0 ; i < particleBests.length; i++) {
    Point3D p = particleBests[i];
    ellipse(p.x, p.y, 10, 10);
  }
  stroke(180, 180, 180, 150);
  for (int i = 0 ; i < particlePositions.length; i++) {
    Point3D p = particlePositions[i][0];
    ellipse(p.x, p.y, 10, 10);
  }
  stroke(180, 120, 150, 150);
  for (int i = 0 ; i < particlePositions.length; i++) {
    Point3D p = particlePositions[i][frameCount%frames];
    ellipse(p.x, p.y, 10, 10);
  }
  stroke(120, 150, 180, 150);
  for (int i = 0 ; i < patternPositions.length; i++) {
    Point3D p = patternPositions[i];
    Point3D p2 = particlePositions[patternMembership[i][frameCount%frames]][frameCount%frames];
    ellipse(p.x, p.y, 4, 4);
    line(p.x, p.y, p2.x, p2.y);
  }
  fill(255);
  text(frameCount%frames, 20, 20);
}

class Point3D {
  float x, y, z;
  Point3D(float inX, float inY, float inZ) {
    this.x = inX;
    this.y = inY;
    this.z = inZ;
  }
}

