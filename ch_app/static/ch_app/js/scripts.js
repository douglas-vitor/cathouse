const menu = {
 target: document.querySelector('.menu-container'),
 targetIgnition: document.querySelector('.menu-nav'),
 open() {
  menu.target.style.opacity = 1
  menu.target.style.visibility = "visible"
  menu.target.style.display = "initial"
  menu.targetIgnition.setAttribute('onclick', 'menu.close()')
 },
 close() {
  menu.target.style.opacity = 0
  menu.target.style.visibility = "hidden"
  menu.target.style.display = "none"
  menu.targetIgnition.setAttribute('onclick', 'menu.open()')
 }
}

const switchButton = {
 on(id) {
  id = String(id)
  const target = document.querySelector(`#${id}`)

  target.classList.add('powerOn')
  target.style.justifyContent = "flex-end"
  target.setAttribute('onclick', `switchButton.off('${id}')`)
 },
 off(id) {
  id = String(id)
  const target = document.querySelector(`#${id}`)

  target.style.justifyContent = "flex-start"
  target.classList.remove('powerOn')
  target.setAttribute('onclick', `switchButton.on('${id}')`)
 }
}


const padlockButton = {
 open(id) {
  id = String(id)
  let target = document.querySelector(`#${id}`)

  target.children[0].classList.remove('closed')
  target.children[0].classList.add('open')
  target.setAttribute('onclick', `padlockButton.closed('${id}')`)
 },
 closed(id) {
  id = String(id)
  let target = document.querySelector(`#${id}`)

  target.children[0].classList.remove('open')
  target.children[0].classList.add('closed')
  target.setAttribute('onclick', `padlockButton.open('${id}')`)
 }
}


const switchButtonClock = {
 on(id) {
  id = String(id)
  const target = document.querySelector(`#${id}`)
  const targetHidden = document.querySelector(`#hidden_${id}`)

  target.classList.add('powerOn')
  target.style.justifyContent = "flex-end"
  target.setAttribute('onclick', `switchButtonClock.off('${id}')`)
  targetHidden.setAttribute('value', 'yes')
 },
 off(id) {
  id = String(id)
  const target = document.querySelector(`#${id}`)
  const targetHidden = document.querySelector(`#hidden_${id}`)

  target.style.justifyContent = "flex-start"
  target.classList.remove('powerOn')
  target.setAttribute('onclick', `switchButtonClock.on('${id}')`)
  targetHidden.setAttribute('value', 'no')
 }
}