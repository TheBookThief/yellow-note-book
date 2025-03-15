const Title = () => {
    const containerStyle = {
        display: 'block',
        height: '15vh',
        width: '100%',
        margin: '0',
        backgroundColor: '#f5d602',
        paddingTop: 20
    };

    const innerContainerStyle = {
        maxWidth: 900
    }

    const logoStyle = {
        height: 50,
        marginTop: 10
    }

    return (<div style={containerStyle} align='center'>
        <div style={innerContainerStyle} align='left'><img style={logoStyle} src='/logo2.png'></img></div>
    </div>)
}

export default Title