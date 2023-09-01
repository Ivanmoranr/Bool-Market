from graph_generator import *


def gen_x_y(l=round(0.4*50),pattern=["rising_wedge","falling_wedge","double_top","double_bottom"]):
    X=[]
    y=[]
    pat={"rising_wedge":1,
            "falling_wedge":2,
            "double_top":3,
            "double_bottom":4
        }
    for i in range(l):

        func={"rising_wedge":rising_wedge(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "falling_wedge":falling_wedge(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "double_top":double_top(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "double_bottom":double_bottom(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            }

        date, ope, hig, low, close, start, end = func[pattern]
        ope=np.array(ope)
        hig=np.array(hig)
        low = np.array(low)
        close = np.array(close)
        X.append(np.column_stack((ope, hig, low, close)))
        y.append((start, end, pat[pattern]))

    for i in range(l):
        if pattern == "rising_wedge":
            m= np.random.randint(0,10)
            m = str(m)
            func={"0":double_bottom(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "1":double_top(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "2":bearish_flag(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2=0),
            "3":bullish_flag(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2=0),
            "4":cup_handle(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "5":head_shoulders(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "6":inv_head_shoulders(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "7":triple_top(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "8":triple_bottom(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "9":norm_params(ar1=0.95, ar2=0, diff=0, n=500, mu=0, sigma=1, h=2)
            }
            date, ope, hig, low, close, start, end = func[m]
            ope=np.array(ope)
            hig=np.array(hig)
            low = np.array(low)
            close = np.array(close)
            X.append(np.column_stack((ope, hig, low, close)))
            y.append((-1, -1, 0))

        if pattern == "falling_wedge":
            m= np.random.randint(0,10)
            m = str(m)
            func={"0":double_bottom(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "1":double_top(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "2":bearish_flag(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2=0),
            "3":bullish_flag(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2=0),
            "4":cup_handle(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "5":head_shoulders(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "6":inv_head_shoulders(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "7":triple_top(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "8":triple_bottom(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "9":norm_params(ar1=0.95, ar2=0, diff=0, n=500, mu=0, sigma=1, h=2)
            }
            date, ope, hig, low, close, start, end = func[m]
            ope=np.array(ope)
            hig=np.array(hig)
            low = np.array(low)
            close = np.array(close)
            X.append(np.column_stack((ope, hig, low, close)))
            y.append((-1, -1, 0))

        if pattern == "double_top":
            m= np.random.randint(0,10)
            m = str(m)
            func={"0":bearish_flag(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2=0),
            "1":bullish_flag(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2=0),
            "2":bullish_pennant(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "3":bearish_pennant(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "4":descending_triangle(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "5":ascending_triangle(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "6":cup_handle(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "7":falling_wedge(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "8":rising_wedge(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "9":norm_params(ar1=0.95, ar2=0, diff=0, n=500, mu=0, sigma=1, h=2)
            }
            date, ope, hig, low, close, start, end = func[m]
            ope=np.array(ope)
            hig=np.array(hig)
            low = np.array(low)
            close = np.array(close)
            X.append(np.column_stack((ope, hig, low, close)))
            y.append((-1, -1, 0))

        if pattern == "double_bottom":
            m= np.random.randint(0,10)
            m = str(m)
            func={"0":bearish_flag(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2=0),
            "1":bullish_flag(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2=0),
            "2":bullish_pennant(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "3":bearish_pennant(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "4":descending_triangle(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "5":ascending_triangle(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "6":cup_handle(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "7":falling_wedge(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "8":rising_wedge(n=500, mu=3, sigma=5, h=1, noise_level=2, ar1 = 0.95, ar2 = 0),
            "9":norm_params(ar1=0.95, ar2=0, diff=0, n=500, mu=0, sigma=1, h=2)
            }
            date, ope, hig, low, close, start, end = func[m]
            ope=np.array(ope)
            hig=np.array(hig)
            low = np.array(low)
            close = np.array(close)
            X.append(np.column_stack((ope, hig, low, close)))
            y.append((-1, -1, 0))

    return X, y

def get_X_y():
    amount={"rising_wedge":556,
        "falling_wedge":268,
        "double_top": 393,
        "double_bottom": 348}
    X_ris_wedg, y_ris_wedg = gen_x_y(l=round(amount["rising_wedge"]*0.4), pattern="rising_wedge")
    X_fal_wedg, y_fal_wedg = gen_x_y(l=round(amount["falling_wedge"]*0.4), pattern="falling_wedge")
    X_d_top, y_d_top = gen_x_y(l=round(amount["double_top"]*0.4), pattern="double_top")
    X_d_bottom, y_d_bottom = gen_x_y(l=round(amount["double_bottom"]*0.4), pattern="double_bottom")
    return X_ris_wedg, y_ris_wedg, X_fal_wedg, y_fal_wedg, X_d_top, y_d_top, X_d_bottom, y_d_bottom
