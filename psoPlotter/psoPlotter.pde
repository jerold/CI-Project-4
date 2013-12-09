import java.io.*;
import java.util.Arrays;

Point3D[] particleBests;
Point3D[][] particlePositions;
Point3D[] patternPositions;
int[][] patternMembership;

float xMin, xMax, yMin, yMax;
int frames;

void setup() {
  int windowSize = 200;
  int edgeWidth = 10;
  size(windowSize + 2*edgeWidth, windowSize + 2*edgeWidth);
  
  xMin = 99999.9;
  xMax = 0.0;
  yMin = 99999.9;
  yMax = 0.0;
 
  try {
    String lines[] = loadStrings("psoMembers.csv");
    println("there are " + lines.length + " lines");
    float[] numbers = float(split(lines[0], ','));
    frames = 0;
    if (lines.length > 1)
      frames = split(lines[10], ',').length/2; // x and y values so divide this by 2
    println("Frames: " + frames);
    
    // Initialize all of the particles and patterns
    int partCount = int(numbers[0]);
    int partStart = 1;
    int partLength = 2;
    println("Particles: " + partCount);
    particleBests = new Point3D[partCount];
    particlePositions = new Point3D[partCount][frames];
    for (int i = 0 ; i < partCount; i++) {
      Point3D p = new Point3D(numbers[i*partLength+partStart], numbers[i*partLength+partStart+1], 0);
//      println(i + ": " + p.x + ", " + p.y + ", " + p.z);
      particleBests[i] = p;
      
      if (p.x > xMax)
        xMax = p.x;
      if (p.x < xMin)
        xMin = p.x;
      if (p.y > yMax)
        yMax = p.y;
      if (p.y < yMin)
        yMin = p.y;
      
      if (frames > 0) {
        float[] positionNumbers = float(split(lines[i+1], ','));
        for (int j = 0 ; j < frames; j++) {
          p = new Point3D(positionNumbers[j*2], positionNumbers[j*2+1], 0);
          particlePositions[i][j] = p;
  
          if (p.x > xMax)
            xMax = p.x;
          if (p.x < xMin)
            xMin = p.x;
          if (p.y > yMax)
            yMax = p.y;
          if (p.y < yMin)
            yMin = p.y;
        }
      }
    }
    
    int patCount = int(numbers[partCount*(partLength)+partStart]);
    int patStart = partCount*(partLength)+partStart + 1;
    int patLength = 3;
    println("Patterns: " + patCount);
    patternPositions = new Point3D[patCount];
    patternMembership = new int[patCount][frames];
    for (int i = 0 ; i < patCount; i++) {
      if (i*patLength+patStart+2 >= numbers.length)
        println((i*patLength+patStart+2)/patLength + " is too big!");
      Point3D p = new Point3D(numbers[i*patLength+patStart], numbers[i*patLength+patStart+1], numbers[i*patLength+patStart+2]);
//      println(i + ": " + p.x + ", " + p.y + ", " + p.z);
      patternPositions[i] = p;
      
      if (p.x > xMax)
        xMax = p.x;
      if (p.x < xMin)
        xMin = p.x;
      if (p.y > yMax)
        yMax = p.y;
      if (p.y < yMin)
        yMin = p.y;

      if (frames > 0) {
        float[] membershipNumbers = float(split(lines[partCount+i+1], ','));
        for (int j = 0 ; j < frames; j++) {
          patternMembership[i][j] = int(membershipNumbers[j]);
        }
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
//  background(40);
  background(255);
  
  fill(0, 0);
//  stroke(120, 180, 150, 150);
  stroke(0, 150);
  strokeWeight(2);
  for (int i = 0 ; i < particleBests.length; i++) {
    Point3D p = particleBests[i];
    ellipse(p.x, p.y, 14, 14);
  }
  if (frames > 0) {
//    stroke(180, 180, 180, 150);
    stroke(0, 150);
    for (int i = 0 ; i < particlePositions.length; i++) {
      Point3D p = particlePositions[i][0];
      ellipse(p.x, p.y, 6, 6);
    }
//    stroke(180, 120, 150, 150);
    stroke(0, 150);
    for (int i = 0 ; i < particlePositions.length; i++) {
      Point3D p = particlePositions[i][frameCount%frames];
      ellipse(p.x, p.y, 10, 10);
    }
  }
  for (int i = 0 ; i < patternPositions.length; i++) {
    Point3D p = patternPositions[i];
    Point3D p2 = particleBests[int(p.z)];
//    stroke(120, 150, 180, 150);
    stroke(0, 50);
    if (frames > 0) {
//      stroke(120+50*patternMembership[i][frameCount%frames], 255-150*patternMembership[i][frameCount%frames], 50+180/(1+(2*patternMembership[i][frameCount%frames])), 150);
      p2 = particlePositions[patternMembership[i][frameCount%frames]][frameCount%frames];
    }
    ellipse(p.x, p.y, 4, 4);
    line(p.x, p.y, p2.x, p2.y);
  }
  fill(255);
//  if (frames > 0)
//    text(frameCount%frames, 10, 20);
//  text(frames, 10, height - 10);
}

class Point3D {
  float x, y, z;
  Point3D(float inX, float inY, float inZ) {
    this.x = inX;
    this.y = inY;
    this.z = inZ;
  }
}

