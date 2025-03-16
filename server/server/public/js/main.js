const tryit = () => {
    const element = document.getElementById('panel');
    const encode = document.getElementById('encode');
    const decode = document.getElementById('decode');
    panel.style.display = 'block';
    encode.style.display = 'none'
    decode.style.display = 'none'
    element.scrollIntoView({ behavior: 'smooth' });
}

const showEncode = () => {
    const panel = document.getElementById('panel');
    const encode = document.getElementById('encode');
    const decode = document.getElementById('decode');
    panel.style.display = 'none';
    encode.style.display = 'block'
    decode.style.display = 'none';
}

const showDecode = () => {
    const panel = document.getElementById('panel');
    const encode = document.getElementById('encode');
    const decode = document.getElementById('decode');
    panel.style.display = 'none';
    encode.style.display = 'none';
    decode.style.display = 'block' 
}