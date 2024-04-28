class Cloze {
  parse(element) {
    const clozeRegex = /\[([^\]]+)\]/g;
    let text = element.innerHTML;
    let parsedHtml = text.replace(clozeRegex, (match, content) => {
      const parts = Cloze._parts(content);
      return this._createToggleButton(parts);
    });    
    element.innerHTML = parsedHtml;
  }

  static _parts(content){
    let parts = content.split('|').map(part => part.trim());
    return parts;
  }
  
  _createToggleButton(parts) {
    let toggleId = Cloze._randomId();
    let partsString = "['" + parts.join("','") + "']"
    let buttonHTML = `
      <button 
         class="cloze" 
         id="${toggleId}" 
         onclick="Cloze._toggleContent(this, ${partsString})" 
         data-toggle-index="0"
      >
        ${Cloze._getButtonContent(parts[0])}
      </button>
    `;
    return buttonHTML;
  }

  static _randomId(){
    return `toggle-${Math.random().toString(36).substr(2, 9)}`
  }
  
  static _toggleContent(button, contents) {
    let index = parseInt(button.getAttribute('data-toggle-index'), 10);
    index = (index + 1) % contents.length;
    button.setAttribute('data-toggle-index', index.toString());
    button.innerHTML = Cloze._getButtonContent(contents[index]);
  }

  static _getButtonContent(content) {
    if (content === '') {
      return `<span 
         class="cloze-placeholder"
      >
         &nbsp;
      </span>`;
    } else if (content.endsWith('.png')) {
      return `<img 
         class="cloze-image"
         src="${content}" 
         alt="${content}"          
      >`;
    } else {
      return `<span 
         class="cloze-content"
      >
         ` + content + `
      </span>`;
    }
  }
}

const cloze = new Cloze();

document.addEventListener('DOMContentLoaded', function() {
  let clozeContainer = document.getElementById('cloze');
  cloze.parse(clozeContainer);
});