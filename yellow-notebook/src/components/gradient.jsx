const Gradient = () => {
    const gradientStyle = {
        display: 'block',
        height: '85vh',
        width: '100%',
        margin: '0',
        background: 'linear-gradient(to bottom,#d7b700,rgb(250, 223, 73))' 
    };

    const containerStyle = {
        maxWidth: 900,
        paddingTop: 100
    }

    const imageStyle = {
        transform: 'rotate(7.5deg)',
        filter: 'drop-shadow(5px 5px 4px #222222)',
        position: 'relative',
        right: 0
    }

    return (<div style={gradientStyle} align='center'>
        <div style={containerStyle} align='left'>
            <img style={imageStyle} src='/yellow.png'></img>
        </div>
    </div>)
}

export default Gradient