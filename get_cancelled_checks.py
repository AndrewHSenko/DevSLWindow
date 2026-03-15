def get_cancelled_checks(start, end):
    query = f'''
    SELECT ch.OpenDate, ch.CheckNo, ch.CheckID, vh.VoidID, iv.MenuID, iv.Quantity
    FROM ((Squirrel.dbo.X_CheckHeader AS ch
    JOIN Squirrel.dbo.X_VoidHeader AS vh ON ch.CheckID = vh.CheckID)
    JOIN Squirrel.dbo.X_ItemVoids AS iv ON vh.VoidID = iv.VoidID)
    WHERE ch.OpenDate BETWEEN '{start}' AND '{end}'
    ORDER BY OpenDate ASC
    '''
    return query