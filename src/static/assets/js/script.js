
const animals = {
    'đ­': 'đ',
    'đś': 'đ',
    'đˇ': 'đ',
    'đŽ': 'đ',
    'đŻ': 'đ',
    'đ': 'đ',
    'đľ': 'đ',
    'đ˛': 'đ',
    'đ´': 'đ',
    'đ°': 'đ',
}

const dom = {
  wholeBody: document.querySelector(".whole-body"),
  bingo: document.querySelector(".bingo"),
  again: document.querySelector(".again"),
  faces: Array.from(document.querySelectorAll(".face")),
  slider: document.querySelector(".slider")
};

const animation = {
  frameOut: () => {
    return new Promise(resolve => {
      // dom.bingo.style.visibility = 'hidden'
      // when frame out animation
      new TimelineMax()
        .to(dom.bingo, 0, { visibility: "hidden" })
        .to(dom.slider, 1, { scale: 0 }, "t1")
        .staggerTo(dom.faces, 1, { scale: 0 }, "t1")
        .to(dom.wholeBody, 1, { scale: 0 }, "t1")
        .timeScale(5)
        .eventCallback("onComplete", resolve);
    });
  },
  frameIn: () => {
    return new Promise(resolve => {
      // ĺźĺąćśćťĺéťčŽ¤éä¸­ĺ¨ćĺˇŚäž§ čä¸ćŻä¸ä¸ĺąçä˝ç˝Ž
      // dom.slider.style.left = '0px'
      new TimelineMax()
        .to(dom.slider, 0, { left: "0px" })
        .to(dom.wholeBody, 1, { scale: 1, delay: 1 })
        .staggerTo(dom.faces, 1, { scale: 1 }, 0.25)
        .to(dom.slider, 1, { scale: 1 })
        .timeScale(5)
        .eventCallback("onComplete", resolve);
    });
  },
  moveSlider: position => {
    return new Promise(resolve => {
      // dom.slider.style.left = (25 + 60) * position + 'px'
      // move and select animation
      new TimelineMax()
        .to(dom.slider, 1, { scale: 0.3 })
        .to(dom.slider, 1, { left: (25 + 60) * position + "px" })
        .to(dom.slider, 1, { scale: 1 })
        .timeScale(5)
        .eventCallback("onComplete", resolve);
    });
  },
  showBingo: () => {
    return new Promise(resolve => {
      // dom.bingo.style.visibility = 'visible'
      // bingo animation
      new TimelineMax()
        .to(dom.bingo, 0, { visibility: "visible" })
        .to(dom.bingo, 1, { rotation: -5 })
        .to(dom.bingo, 1, { rotation: 5 })
        .to(dom.bingo, 1, { rotation: 0 })
        .timeScale(8)
        .eventCallback("onComplete", resolve);
    });
  }
};

let options = [];
let answer = [];
let canSelect = false;

async function newGame() {
  await animation.frameOut();
  shuffle();
  await animation.frameIn();
  canSelect = true;
}

// shuffle()ĺ˝ć°éćşçäťanimalsć°çťä¸­éĺş5ä¸Şĺ¨çŠćžĺ¨dom.facesä¸­ ĺäťĺśä¸­éĺşä¸ä¸Şçĺ¨čşŤĺćžĺ¨dom.wholeBodyä¸­
function shuffle() {
  options = _.slice(_.shuffle(_.entries(animals)), -5);
  answer = _.sample(_.slice(options, -4));

  dom.faces.forEach((face, i) => {
    face.innerText = options[i][0];
  });
  dom.wholeBody.innerText = answer[1];
}

async function select(e) {
  if (!canSelect) return;

  let position = _.findIndex(options, x => x[0] == e.target.innerText);
  await animation.moveSlider(position);

  if (animals[e.target.innerText] == answer[1]) {
    // éćŠć­ŁçĄŽĺşç°ćç¤şčŻ­ĺ ĺśäťĺ¤´ĺä¸ĺŻĺçšĺť
    canSelect = false;
    await animation.showBingo();
  }
}

function init() {
  dom.faces.forEach(face => {
    face.addEventListener("click", select);
  });
  dom.again.addEventListener("click", newGame);
  newGame();
}
window.onload = init;