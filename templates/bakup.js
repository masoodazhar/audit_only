function lastLogic(auditColumns){
    var table = document.getElementById('bankTbody');
    var bankRows = table.getElementsByTagName('tr');  


    var selectedColumnsAudit = []
    auditColumns.forEach((itemName, i)=>{
        var checks = document.getElementById("auditTbody")
    
        selectedColumnsAudit[i] = checks.getElementsByClassName(itemName);
    })

    finalMatched = []
    
    var RowsColumns = [] 

    for (var col=0; col<selectedColumnsAudit.length; col++){
        
        for (var row=0; row<selectedColumnsAudit[col].length; row++){
            
             RowsColumns[col] = selectedColumnsAudit[col]
        }
        
    }
    
//   console.table(RowsColumns);
    // console.table(transpose(selectedColumnsAudit));
    for (var col=0; col<selectedColumnsAudit.length; col=1){
        for (var row=0; row<RowsColumns[col].length; row++){

            singleRowsData = []

            for(var f=0; f<RowsColumns.length; f++){
                
                
                singleRowsData.push(RowsColumns[f][row])
               
            }
            
            for (var i=0, length = bankRows.length; i<length; i++) {
                

                matches = 0
                var tds = bankRows[i].getElementsByTagName('td');
                for(var td of tds){
                    needToFindValues = singleRowsData.map(x => x.innerText)
                    targetValue = td.innerText
                    if(needToFindValues.includes(targetValue) ){
                        matches++
                        
                        // console.log(`target = ${targetValue},   find = ${needToFindValue}`);
                        if (matches >= singleRowsData.length){
                            console.log('iiiifffff=========================',bankRows[i]);
                            bankRows[i].classList.add('bg-success')
                            bankRows[i].classList.add('text-white')
                           
                            finalMatched.push(
                                [targetValue]
                            ) 
                        }else{
                            console.log('eeeeellllsssseee==================',bankRows[i]);
                            bankRows[i].classList.remove('bg-success')
                            bankRows[i].classList.remove('text-white')
                        }
                    }
                }
            }
            // console.log(Array.from(singleRowsData));
            // break
        }
        break
    }

    // console.table(finalMatched);
    // for(var f=0; f<RowsColumns.length; f++){
        // console.log(RowsColumns[f][0]);
        // for ( var val of rows){
        //     var needToFindValue = val.innerText
            
            // for (var i=0, length = bankRows.length; i<length; i++) {
            //     matches = 0
            //     var tds = bankRows[i].getElementsByTagName('td');
            //     for(var td of tds){
            //         targetValue = td.innerText
            //         if(targetValue == needToFindValue){
            //             // console.log(`target = ${targetValue},   find = ${needToFindValue}`);
            //             finalMatched.push(
            //                 [targetValue, val]
            //             ) 
            //         }
            //     }
            // }
        // }
    // }

    // console.log(finalMatched);
    

    
}
