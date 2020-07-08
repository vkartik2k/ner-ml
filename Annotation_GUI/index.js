let container = document.getElementsByClassName('container')[0]

let god = []
let arr = []
let start = 0
let prevStart = 0
let sentence = []
let step = 0
let startStop = -1

const init = () => document.getElementById('fileInput').addEventListener('change', handleFileSelect, false)

function handleFileSelect(event) {
    const reader = new FileReader()
    reader.onload = handleFileLoad
    reader.readAsText(event.target.files[0])
}

function download() {
    filename='dataset.csv'
    var element = document.createElement('a')
    let str = ''
    god.forEach(ele => str += ele[0]+','+ele[1])
    element.setAttribute('href', 'data:text/plaincharset=utf-8,' + encodeURIComponent(str))
    element.setAttribute('download', filename)

    element.style.display = 'none'
    document.body.appendChild(element)

    element.click()

    document.body.removeChild(element)
}

function reloadStep() {
    if (step == 0) {
        document.getElementById('currentHead').innerHTML = `Step : <span style="color: rgb(0, 187, 187) font-weight: bold">Choose
        Locations</span>`
    }
    if (step == 1) {
        document.getElementById('currentHead').innerHTML = `Step : <span style="color: rgb(0, 187, 187) font-weight: bold">Choose
        Organisations</span>`
    }
    if (step == 2) {
        document.getElementById('currentHead').innerHTML = `Step : <span style="color: rgb(0, 187, 187) font-weight: bold">Choose
        Persons</span>`
    }
}

function mark(i) {
    if(startStop==-1) {
        startStop = i
        document.getElementById('ele' + (prevStart+startStop)).className += ' selected'
    }
    else {
        if(step==0) {
            god[prevStart+startStop][1] = 'B-LOC\n'
            document.getElementById('ele' + (prevStart+startStop)).className = 'I-LOC'
        }
        if(step==1) {
            god[prevStart+startStop][1] = 'B-ORG\n'
            document.getElementById('ele' + (prevStart+startStop)).className = 'B-ORG'
        }
        if(step==2) {
            god[prevStart+startStop][1] = 'B-PER\n'
            document.getElementById('ele' + (prevStart+startStop)).className = 'B-PER'
        }
        for(let j=startStop+1; j<=i; j++) {
            if(step==0) {
                god[prevStart+j][1] = 'I-LOC\n'
                document.getElementById('ele' + (prevStart+j)).className = 'I-LOC'
            }
            if(step==1) {
                god[prevStart+j][1] = 'I-ORG\n'
                document.getElementById('ele' + (prevStart+j)).className = 'I-ORG'
            }
            if(step==2) {
                god[prevStart+j][1] = 'I-PER\n'
                document.getElementById('ele' + (prevStart+j)).className = 'I-PER'
            }
        }
        startStop = -1
    }
}

function next_sentence() {
    step = 0
    reloadStep()
    sentence = []
    prevStart = start
    document.getElementById('sentenceNo').innerHTML = arr[start]
    god.push(arr[start].split(','))
    start += 1
    while (!arr[start].includes("Sentence #")) {
        sentence.push(arr[start].split(','))
        god.push(arr[start].split(','))
        start += 1
    }
    innerPart = ``
    let i = 0
    sentence.forEach(element => {
        innerPart += "<button id='ele"+(i+prevStart)+"' class=" + element[1] + " onclick= mark("+i+")> " + element[0] + " </button>"
        i++
    })
    container.innerHTML = innerPart
}

function next() {
    step += 1
    if (step == 3) step = 0
    reloadStep()
}

function handleFileLoad(event) {
    let text = event.target.result
    arr = text.split('\n')
    next_sentence()
}

let resetMark = () => {
    if(startStop != -1) document.getElementById('ele' + (prevStart+startStop)).classList.remove("selected")
    startStop = -1
}

let markO = () => {
    for(let i=0; i<sentence.length; i++) {
        god[prevStart+i][1] = 'O\n'
        document.getElementById('ele' + (prevStart+i)).className = ''
    }
}

Mousetrap.bind('n', next)
Mousetrap.bind('m', next_sentence)
Mousetrap.bind('r',resetMark)
Mousetrap.bind('d',download)
Mousetrap.bind('o',markO)