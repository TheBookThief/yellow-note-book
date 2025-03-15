import { useCallback, useEffect, useState } from "react";
import Particles, { initParticlesEngine } from "@tsparticles/react";
import { loadFull } from "tsparticles";

const Particle = () => {
    const [ init, setInit ] = useState(false);

    useEffect(() => {
        initParticlesEngine(async (engine) => {
            await loadFull(engine);
        }).then(() => {
            setInit(true);
        });
    }, []);

    const particlesLoaded = (container) => {
    };

    const divStyle = {
        display: 'inline-block',
        position: 'static',
        height: '85vh',
        width: '100%', 
    };

    return (
        <div style={divStyle}>
            <Particles
                id="tsparticles"
                particlesLoaded={particlesLoaded}
                options={{
                    fpsLimit: 120,
                    interactivity: {
                        events: {
                            resize: true,
                        },
                    },
                    particles: {
                        number: {
                            value: 150,  // Number of particles
                            density: {
                                enable: true,
                                value_area: 20,
                            },
                        },
                        /*links: {
                            enable: true,
                            distance: 150,
                            opacity: 1,
                            width: 1,
                        },*/
                        color: {
                            value: '#dec431',
                        },
                        shape: {
                            type: 'circle',  // Specify that the particle shape will be an image
                        },
                        opacity: {
                            value: 1,
                        },
                        size: {
                            value: 10,  // Size of each particle (image size)
                        },
                        move: {
                            enable: true,
                            speed: 1,
                            direction: 'none',
                        },
                    },
                detectRetina: true,
            }}
        />
        </div>
    )
};

export default Particle