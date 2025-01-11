
function setupTypewriter(t) {
    var HTML = t.innerHTML;

    t.innerHTML = "";

    var cursorPosition = 0,
        tag = "",
        writingTag = false,
        tagOpen = false,
        typeSpeed = 100,
        tempTypeSpeed = 0;

    var type = function() {
        // Skip the img block
        // if (HTML.slice(cursorPosition, cursorPosition + 4) === "<img") {
        //     // Extract the <img> tag
        //     let imgTag = "";
        //     while (HTML[cursorPosition] !== ">" && cursorPosition < HTML.length) {
        //         imgTag += HTML[cursorPosition];
        //         cursorPosition++;
        //     }
        //     imgTag += ">"; // Include the closing ">"

        //     // Append the <img> element to the DOM
        //     const div = document.createElement("div");
        //     div.innerHTML = imgTag;
        //     t.appendChild(div.firstChild);

        //     cursorPosition++; // Move past the closing ">"
        //     return type(); // Restart the typing loop
        // }

        if (writingTag === true) {
            tag += HTML[cursorPosition];
        }

        if (HTML[cursorPosition] === "<") {
            tempTypeSpeed = 0;
            if (tagOpen) {
                tagOpen = false;
                writingTag = true;
            } else {
                tag = "";
                tagOpen = true;
                writingTag = true;
                tag += HTML[cursorPosition];
            }
        }
        if (!writingTag && tagOpen) {
            tag.innerHTML += HTML[cursorPosition];
        }
        if (!writingTag && !tagOpen) {
            if (HTML[cursorPosition] === " ") {
                tempTypeSpeed = 0;
            }
            else {
                tempTypeSpeed = (Math.random() * typeSpeed) + 60;
            }
            t.innerHTML += HTML[cursorPosition];
        }
        if (writingTag === true && HTML[cursorPosition] === ">") {
            tempTypeSpeed = (Math.random() * typeSpeed) + 60;
            writingTag = false;
            if (tagOpen) {
                var newSpan = document.createElement("span");
                t.appendChild(newSpan);
                newSpan.innerHTML = tag;
                tag = newSpan.firstChild;
            }
        }

        cursorPosition += 1;
        if (cursorPosition < HTML.length - 1) {
            setTimeout(type, tempTypeSpeed);
        }
    };

    return {
        type: type
    };
}

var typer = document.getElementById('typewriter');

typewriter = setupTypewriter(typer);

typewriter.type();
