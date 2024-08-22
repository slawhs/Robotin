def ajunt_text(text):
    text = text.split("\n")
    i = 0
    while i < len(text):
        if len(text[i]) > 100:
            text.insert(i+1, text[i][100:])
            text[i] = text[i][:100]
        i += 1
    return "\n".join(text)


print(ajunt_text("""
oaooooo

ntreodintr dant unatu notun atruntaore untaeua
au aoeuraoeturnatr ua anutaoeutnran anetur auaoe uaoeu taoe uaoe
uaoeu aoeutrbaoet ua
    taoetunraoetuaeotu anteour nate urnateour aeua oewu atoeb utaobe utaboe utbao eubao eub aoeub aoebu aoteb uaoe
    uaoeu aoteu aoteu atoeu atose uatoe uaoea
    aoenu aoe naeo kaneo kna oekna oenr aso ksan rona roea
    taoetunraoetuaeotu anteour nate urnateour aeua oewu atoeb utaobe utaboe utbao eubao eub aoeub aoebu aoteb uaoe
    taoetunraoetuaeotu anteour nate urnateour aeua oewu atoeb utaobe utaboe utbao eubao eub aoeub aoebu aoteb uaoe
    taoetunraoetuaeotu anteour nate urnateour aeua oewu atoeb utaobe utaboe utbao eubao euboooooooooooooooooooooooooooooooo aoeub aoebu aoteb uaoe
    taoetunraoetuaeotu anteour nate urnateour aeua oewu atoeb utaobe utaboe utbao eubao eub aoeub aoebu aoteb uaoe
    taoetunraoetuaeotu anteour nate urnateour aeua oewu atoeb utaobe utaboe utbao eubao eub aoeub aoebu aoteb uaoe
    taoetunraoetuaeotu anteour nate urnateour aeua oewu atoeb utaobe utaboe utbao eubao eub aoeub aoebu aoteb uaoe
    taoetunraoetuaeotu anteour nate urnateour aeua oewu atoeb utaobe utaboe utbao eubao eub aoeub aoebu aoteb uaoe
                 """))