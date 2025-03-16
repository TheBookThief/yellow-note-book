const tryit = () => {
    const element = document.getElementById('panel');
    element.scrollIntoView({ behavior: 'smooth' });
}

const showEncode = () => {
    const panel = document.getElementById('panel');
    const encode = document.getElementById('encode');
    panel.style.display = 'none';
    encode.style.display = 'block'
}