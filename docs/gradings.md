# Gradings

## Grading System Types

| ID  | Name       |
| --- | ---------- |
| 1   | Free       |
| 2   | Bouldering |

**Resulting Attributes:**

- PK_Id
- Name

## Grading Systems

| ID  | Name | Grading System Type |
| --- | ---- | ------------------- |
| 1   | UIAA | Free                |
| 2   | FB   | Bouldering          |
| 3   | Sax  | Free                |
| n   | ...  | ...                 |

**Resulting Attributes:**

- PK_Id
- FK_Grading_System_Type
- Name

## Grades

| GradingSystem | Name | Weight |
| ------------- | ---- | ------ |
| UIAA          | 1    | 1      |
| UIAA          | 2    | 2      |
| Fontainbleau  | 4a   | 4      |

**Resulting Attributes:**

- PK_Id
- FK_Grading_System
- Name 
- Weight ... used for comparison (see below)

## Comparing Grades


Comparing grades is a difficult topic and is always subjectiv. So let's see it more as a guideline than a hard rule-set.

### Free Climbing example

| i   | Sierra(USA) | UK_Tech | UK_Adj | France | UIAA | Australia | Saxony | Skandinavia | Brasil |
| --- | ----------- | ------- | ------ | ------ | ---- | --------- | ------ | ----------- | ------ |
| 0   |             |         |        |        |      |           |        |             |        |
| 1   | 5.2         |         |        | 1      | 1    |           | I      |             | Isup   |
| 2   |             |         |        |        |      |           |        |             |        |
| 3   | 5.3         |         |        | 2      | 2    | 11        | II     |             | II     |
| 4   |             |         |        |        |      |           |        |             |        |
| 5   | 5.4         |         |        | 3      | 3    | 12        | III    |             | IIsup  |
| 6   |             |         |        |        |      |           |        |             |        |
| 7   | 5.5         | 4a      | VD     | 4      | 4    |           | IV     |             | III    |
| 8   |             |         |        |        |      |           |        |             |        |
| 9   | 5.6         |         | S      | 5a     | 5-   | 13        | V      | 5−          | IIIsup |
| 10  |             |         |        |        |      |           |        |             |        |
| 11  | 5.7         | 4b      | HS     |        | 5    | 14        | VI     | 5           | IV     |
| 12  |             | 4c      |        | 5b     | 5+   | 15        |        |             |        |
| 13  | 5.8         |         | VS     |        | 6-   | 16        | VIIa   | 5+          | IVsup  |
| 14  |             |         |        |        |      |           |        |             |        |
| 15  | 5.9         | 5a      | HVS    | 5c     | 6    | 17        | VIIb   |             | V      |
| 16  |             |         |        |        |      |           |        |             |        |
| 17  | 5.10a       |         | E1     | 6a     | 6+   | 18        | VIIc   | 6−          | Vsup   |
| 18  |             |         |        |        |      |           |        |             |        |
| 19  | 5.10b       | 5b      |        | 6a+    | 7-   | 19        | VIIIa  |             | VI     |
| 20  |             |         |        |        |      |           |        |             |        |
| 21  | 5.10c       |         | E2     | 6b     | 7    | 20        | VIIIb  | 6           |        |
| 22  |             |         |        |        |      |           |        |             |        |
| 23  | 5.10d       | 5c      |        | 6b+    | 7+   | 21        | VIIIc  |             | VIsup  |
| 24  |             |         |        |        |      |           |        |             |        |
| 25  | 5.11a       |         | E3     | 6c     |      | 22        |        | 6+          | VIIa   |
| 26  |             |         |        |        |      |           |        |             |        |
| 27  | 5.11b       |         |        | 6c+    | 8−   | 23        | IXa    |             |        |
| 28  |             |         |        |        |      |           |        |             |        |
| 29  | 5.11c       | 6a      | E4     | 7a     | 8    | 24        | IXb    | 7−          | VIIb   |
| 30  |             |         |        |        |      |           |        |             |        |
| 31  | 5.11d       |         |        | 7a+    | 8+   | 25        | IXc    | 7           | VIIc   |
| 32  |             |         |        |        |      |           |        |             |        |
| 33  | 5.12a       |         | E5     | 7b     |      | 26        |        | 7+          | VIIIa  |
| 34  |             |         |        |        |      |           |        |             |        |
| 35  | 5.12b       | 6b      |        | 7b+    | 9−   |           | Xa     | 8−          | VIIIb  |
| 36  |             |         |        |        |      |           |        |             |        |
| 37  | 5.12c       |         | E6     | 7c     | 9    | 27        | Xb     | 8           | VIIIc  |
| 38  |             |         |        |        |      |           |        |             |        |
| 39  | 5.12d       | 6c      |        | 7c+    | 9+   | 28        | Xc     | 8+          | IXa    |
| 40  |             |         |        |        |      |           |        |             |        |
| 41  | 5.13a       |         | E7     | 8a     |      | 29        |        | 9−          | IXb    |
| 42  |             |         |        |        |      |           |        |             |        |
| 43  | 5.13b       |         |        |        |      |           |        | 9           | IXc    |
| 44  |             |         |        |        |      |           |        |             |        |
| 45  | 5.13c       | 7a      |        | 8a+    | 10−  | 30        | XIa    | 9+          | Xa     |
| 46  |             |         |        |        |      |           |        |             |        |
| 47  | 5.13d       |         | E8     | 8b     | 10   | 31        | XIb    | 10−         | Xb     |
| 48  |             |         |        |        |      |           |        |             |        |
| 49  | 5.14a       |         |        | 8b+    | 10+  | 32        | XIc    | 10          | Xc     |
| 50  |             |         |        |        |      |           |        |             |        |
| 51  | 5.14b       | 7b      |        | 8c     |      | 33        |        | 10+         | XIa    |
| 52  |             |         |        |        |      |           |        |             |        |
| 53  | 5.14c       |         | E9     | 8c+    | 11−  | 34        |        | 11−         | XIb    |
| 54  |             |         |        |        |      |           |        |             |        |
| 55  | 5.14d       | 7c      |        | 9a     | 11   | 35        |        | 11          | XIc    |
| 56  |             |         |        |        |      |           |        |             |        |
| 57  | 5.15a       |         |        | 9a+    |      | 36        |        | 11+         | XIIa   |
| 58  |             |         |        |        | 11+  |           |        |             |        |
| 59  | 5.15b       |         |        | 9b     |      | 37        |        |             | XIIb   |
| 60  | 5.15c       |         |        | 9b+    | 12-  | 38        |        |             | XIIc   |

### Bouldering

analogous