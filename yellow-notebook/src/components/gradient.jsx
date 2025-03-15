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
        marginLeft: 30,
        marginRight: 30,
        paddingTop: 100,
        position: 'relative'
    }

    const imageStyle = {
        transform: 'rotate(7.5deg)',
        filter: 'drop-shadow(5px 5px 4px #222222)',
        position: 'absolute',
        float: 'right',
        right: 0
    }

    const titleStyle = {
        position: 'absolute',
        float: 'left',
        maxWidth: 700,
        paddingTop: 60,
        fontFamily: 'Verdana',
        color: 'White',
        left: 0,
        fontSize: 32
    }

    const subtitleStyle = {
        fontSize: 20
    }

    const coloredStyle = {
        color: 'yellow'
    }

    const buttonStyle = {
        paddingTop: 12,
        paddingBottom: 12,
        paddingLeft: 32,
        paddingRight: 32,
        fontSize: 20,
        marginTop: 20,
        borderRadius: 15,
        cursor: 'pointer',
        border: '2px solid black',
        outline: 'none',
        backgroundColor: '#ffcd00',
        fontWeight: 'bold'
    }

    return (<div style={gradientStyle} align='center'>
        <div style={containerStyle} align='left'>
            <img style={imageStyle} src='/yellow.png'></img>
            <h2 style={titleStyle}>FROM FORMULAS TO FREQUENCIES.<br/>
            <label style={subtitleStyle}>The hidden power of <label style={coloredStyle}>MUSIC</label></label><br/>
            <button style={buttonStyle}>Try it</button></h2>
        </div>
    </div>)
}

export default Gradient