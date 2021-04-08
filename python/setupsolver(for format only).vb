Sub setupsolver()

'NEED TO CHECK THE OPENSOLVER IN TOOLS AS A REFERENCE FOR THIS TO WORK

Dim MaxSpaces As Integer
Dim TotalSpaces As Integer
Dim TotalItems As Integer

Dim counter As Integer
Dim counter2 As Integer

Dim Rng As Range
Dim InputRng As Range, OutRng As Range

Dim Result As OpenSolverResult
Dim ObjFunction As Range

'Delete the Solver Sheet
Application.DisplayAlerts = False 'switching off the alert button
Sheets("Solver Sheet").Delete
Application.DisplayAlerts = True 'switching on the alert button

'Grab the good values
MaxSpaces = Cells(2, 8).Value
TotalSpaces = Cells(4, 8).Value
TotalItems = Cells(6, 8).Value

'Create the new columns
ActiveSheet.Cells(1, 4).Value = "# items/time period"
ActiveSheet.Cells(1, 5).Value = "# items/pallet"
ActiveSheet.Cells(1, 6).Value = "Flow"

'Generate the # items / 2 months column
'counter = 2
'
'For i = 2 To TotalItems + 1
'
'    ActiveSheet.Cells(i, 13).Value = "=sum(D" & counter & ":L" & counter & ")"
'    counter = counter + 1
'
'Next i

'Generate the # items / pallet
counter = 2

For i = 2 To TotalItems + 1

    ActiveSheet.Cells(i, 5).Value = "=B" & counter & " * C" & counter
    counter = counter + 1

Next i

'Generate the Flow
counter = 2

For i = 2 To TotalItems + 1

    ActiveSheet.Cells(i, 6).Value = "=D" & counter & " / E" & counter
    counter = counter + 1

Next i

'Label ranges in Pull from SAP
ActiveWorkbook.Names.Add Name:="MaxSpace", RefersToR1C1:= _
    "='Sheet1'!R2C8"
    
ActiveWorkbook.Names.Add Name:="TotalSpace", RefersToR1C1:= _
    "='Sheet1'!R4C8"

ActiveWorkbook.Names.Add Name:="SKUS", RefersToR1C1:= _
    "='Sheet1'!R6C8"

ActiveWorkbook.Names.Add Name:="SKUS2USE", RefersToR1C1:= _
    "='Sheet1'!R2C1:R1542C1"

'create new sheet
Sheets.Add
ActiveSheet.Name = "Solver Sheet"

'Label ranges in Solver Sheet
ActiveWorkbook.Names.Add Name:="Flow", RefersToR1C1:= _
    "='Solver Sheet'!R2C2:R12329C2"
    
ActiveWorkbook.Names.Add Name:="Choice", RefersToR1C1:= _
    "='Solver Sheet'!R2C4:R12329C4"

'Column labels
ActiveSheet.Cells(1, 1).Value = "SAP #"
ActiveSheet.Cells(1, 2).Value = "Flow"
ActiveSheet.Cells(1, 3).Value = "Spaces"
ActiveSheet.Cells(1, 4).Value = "Zij"
ActiveSheet.Cells(1, 5).Value = "Mult"
ActiveSheet.Cells(1, 6).Value = "Restocks"
ActiveSheet.Cells(1, 7).Value = "Total Restocks"

ActiveSheet.Cells(1, 8).Value = "Check"
ActiveSheet.Cells(2, 8).Value = "SAP #"
ActiveSheet.Cells(2, 9).Value = "Zij"
ActiveSheet.Cells(2, 10).Value = "Spaces"
ActiveSheet.Cells(2, 11).Value = "Total Items"
ActiveSheet.Cells(2, 12).Value = "Total Spaces"

'Duplicate the SKUs and Flow

Sheets("Sheet1").Select

ActiveSheet.Range("A2:A" & TotalItems + 1).Select
Selection.Copy
ActiveSheet.Range("T2").Select
Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False

'Range("A2:A" & TotalItems + 1).Copy Range("T2:T" & TotalItems + 1)

For i = 2 To TotalItems + 1
    Cells(i, 21).Value = 8
Next i


Set InputRng = Application.Selection
Set InputRng = Range("T2:U" & TotalItems + 1)

Sheets("Solver Sheet").Select

Set OutRng = ActiveSheet.Range("A2:A" & TotalItems + 1)
Set OutRng = OutRng.Range("A1")
For Each Rng In InputRng.Rows
    xValue = Rng.Range("A1").Value
    xNum = Rng.Range("B1").Value
    OutRng.Resize(xNum, 1).Value = xValue
    Set OutRng = OutRng.Offset(xNum, 0)
Next

Sheets("Sheet1").Select

'Range("$O$2:$O$" & TotalItems + 1).Copy Range("$T$2:$T$" & TotalItems + 1)
ActiveSheet.Range("F2:F" & TotalItems + 1).Select
Selection.Copy
ActiveSheet.Range("T2").Select
Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False

Set InputRng = Application.Selection
Set InputRng = Range("T2:U" & TotalItems + 1)

Sheets("Solver Sheet").Select

Set OutRng = ActiveSheet.Range("B2:B" & TotalItems + 1)
Set OutRng = OutRng.Range("A1")
For Each Rng In InputRng.Rows
    xValue = Rng.Range("A1").Value
    xNum = Rng.Range("B1").Value
    OutRng.Resize(xNum, 1).Value = xValue
    Set OutRng = OutRng.Offset(xNum, 0)
Next

'Spaces setup

counter = 1 'counter is used to index to the next space

For i = 2 To TotalItems * MaxSpaces + 1

    ActiveSheet.Cells(i, 3).Value = counter
    counter = counter + 1
    
    If counter = MaxSpaces + 1 Then
        counter = 1
    End If

Next i

'Mult

counter = 2

For i = 2 To TotalItems * MaxSpaces + 1

    ActiveSheet.Cells(i, 5).Value = "=C" & counter & " * D" & counter
    counter = counter + 1

Next i

'Setup restocks

counter = 2

For i = 2 To TotalItems * MaxSpaces + 1

    ActiveSheet.Cells(i, 6).Value = "=B" & counter & "/C" & counter & "*D" & counter
    counter = counter + 1

Next i

'Setup total restocks cell

ActiveSheet.Cells(2, 7).Value = "=sum(F2:F" & TotalItems * MaxSpaces + 1 & ")"

'Setup SAP # V2

Sheets("Sheet1").Select
ActiveSheet.Range("T2:U" & TotalItems + 1).Clear
Range("A2:A" & TotalItems + 1).Select
Worksheets("Sheet1").Range("A2:A" & TotalItems + 1).Copy Worksheets("Solver Sheet").Range("H3:H" & TotalItems + 1)
Sheets("Solver Sheet").Select

'Setup Zij V2

counter = 2
counter2 = MaxSpaces + 1

For i = 3 To TotalItems + 2

    ActiveSheet.Cells(i, 9).Value = "=sum(D" & counter & ":D" & counter2 & ")"
    
    counter = counter + MaxSpaces
    
    counter2 = counter2 + MaxSpaces
    
Next i

'Setup Spaces V2

counter = 2
counter2 = MaxSpaces + 1

For i = 3 To TotalItems + 2

    ActiveSheet.Cells(i, 10).Value = "=sum(E" & counter & ":E" & counter2 & ")"
    
    counter = counter + MaxSpaces
    
    counter2 = counter2 + MaxSpaces
    
Next i

'Setup Total items

ActiveSheet.Cells(3, 11).Value = "=count(J3:J" & TotalItems + 2 & ")"

'Setup Total spaces

ActiveSheet.Cells(3, 12).Value = "=sum(E2:E" & TotalItems * MaxSpaces + 1 & ")"

'Setting up the solver
SetChosenSolver ("CBC")

SolverOk SetCell:="$G$2", MaxMinVal:=2, ValueOf:=0, ByChange:="$D$2:$D$" & TotalItems * MaxSpaces + 1, _
        Engine:=1, EngineDesc:="GRG Nonlinear"
        
SolverAdd CellRef:="$I$3:$I$" & TotalItems + 2, Relation:=2, FormulaText:="1"
    
SolverAdd CellRef:="$K$3", Relation:=2, FormulaText:="" & TotalItems

SolverAdd CellRef:="$L$3", Relation:=2, FormulaText:="" & TotalSpaces

SolverAdd CellRef:="$D$2:$D$" & TotalItems * MaxSpaces + 1, Relation:=1, FormulaText:="1"

Result = RunOpenSolver(False, True) ' do not relax IP, do hide dialogs

'Solver's solution to which SKU gets how many spaces PUT AFTER THE SOLVER CODE

counter = 3

For i = 2 To TotalItems * MaxSpaces + 1
    
    If ActiveSheet.Cells(i, 5).Value > 0 Then
    
        ActiveSheet.Cells(counter, 10).Value = ActiveSheet.Cells(i, 5).Value
    
        counter = counter + 1
    
    End If
    
Next i

End Sub
Sub epic()

Dim counter As Integer
Dim counter2 As Integer

counter = 2
counter2 = MaxSpaces + 1

For i = 3 To TotalItems + 2

    ActiveSheet.Cells(i, 10).Value = "=sum(E" & counter & ":E" & counter2 & ")"
    
    counter = counter + MaxSpaces
    
    counter2 = counter2 + MaxSpaces
    
Next i

End Sub
Sub pizza()

SolverOk SetCell:="$G$2", MaxMinVal:=2, ValueOf:=0, ByChange:="$D$2:$D$" & 1541 * 8 + 1, _
        Engine:=1, EngineDesc:="GRG Nonlinear"
        
SolverAdd CellRef:="$I$3:$I$" & 1541 + 2, Relation:=2, FormulaText:="1"
    
SolverAdd CellRef:="$K$3", Relation:=2, FormulaText:="" & 1541

SolverAdd CellRef:="$L$3", Relation:=2, FormulaText:="" & 2688

SolverAdd CellRef:="$D$2:$D$" & 1541 * 8 + 1, Relation:=1, FormulaText:="1"


End Sub

Sub CopyData()
'Updateby Extendoffice
Dim Rng As Range
Dim InputRng As Range, OutRng As Range
xTitleId = "KutoolsforExcel"
Set InputRng = Application.Selection
Set InputRng = Application.InputBox("Range :", xTitleId, InputRng.Address, Type:=8)
Set OutRng = Application.InputBox("Out put to (single cell):", xTitleId, Type:=8)
Set OutRng = OutRng.Range("A1")
For Each Rng In InputRng.Rows
    xValue = Rng.Range("A1").Value
    xNum = Rng.Range("B1").Value
    OutRng.Resize(xNum, 1).Value = xValue
    Set OutRng = OutRng.Offset(xNum, 0)
Next
End Sub

Sub Sum8()

Dim counter As Integer
Dim counter2 As Integer

counter = 2
counter2 = 11

For i = 2 To 12

    ActiveSheet.Cells(i, 10).Value = "=sum(G" & counter & ":G" & counter2 & ")"
    
    counter = counter + 10
    
    counter2 = counter2 + 10
    
Next i

End Sub

Sub proof()

Dim Result As OpenSolverResult
Dim counter As Integer
Dim counter2 As Integer
Dim indexF As Integer
Dim columnNum As Integer

counter = 1
indexF = 16
columnNum = 11
counter2 = 21

For i = 11 To 110

    SolverOk SetCell:="$M$2", MaxMinVal:=2, ValueOf:=0, ByChange:="$G$2:$G$111", _
        Engine:=1, EngineDesc:="GRG Nonlinear"
    
    SolverAdd CellRef:="$O$2", Relation:=2, FormulaText:="" & i
    
    Result = RunOpenSolver(False, True) ' do not relax IP, do hide dialogs
    
    ActiveSheet.Range("K1:M12").Select
    Selection.Copy
    ActiveSheet.Range("Q1").Select
    Selection.PasteSpecial Paste:=xlPasteValues, Operation:=xlNone, SkipBlanks _
        :=False, Transpose:=False
        
    ActiveSheet.Range("S2").Select
    Selection.Copy
    ActiveSheet.Cells(2, counter2).Select
    ActiveSheet.Paste
        
    ActiveSheet.Range("Q1:S12").Select
    Selection.Copy
    
If counter = 6 Then

    indexF = indexF + 14
    columnNum = 11
    counter = 1

End If

If i = 27 Then
counter = counter
End If

    ActiveSheet.Cells(indexF, columnNum).Select 'select the area to put the solution
    ActiveSheet.Paste

    ActiveSheet.Cells(indexF - 1, columnNum).Value = "Total space = " & i

SolverDelete CellRef:="$O$2", Relation:=2, FormulaText:="" & i

counter = counter + 1
counter2 = counter2 + 1
columnNum = columnNum + 4
    
Next i

End Sub




